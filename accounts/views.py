from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import render,  get_object_or_404
from friendship.models import Friend, Follow, Block, FriendshipRequest
import pdb
from django.views.decorators.http import require_POST, require_GET

class Login(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"

class Logout(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/create.html"
    success_url = reverse_lazy('accounts:login')

class Profile(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        display_user = get_object_or_404(User, id=self.kwargs['pk'])
        posts = display_user.post_set.all().order_by('-published_date')
        like_posts = display_user.like_user.all()
        try:
            login_user = self.request.user
            requesting_follows = FriendshipRequest.objects.get(to_user=display_user.id, from_user=login_user.id)
            friends = Friend.objects.are_friends(login_user, display_user)
            following = Follow.objects.following(login_user)
            blocking_user = Block.objects.is_blocked(login_user, display_user)
        except:
            pass

        context['display_user']=display_user
        context['posts']=posts
        context['like_posts']=like_posts
        try:
            context['requesting_follows'] = requesting_follows
            context['login_user']= login_user
            context['friends']=friends
            context['following']=following
            context['blocking_user']=blocking_user
        except:
            pass
        # pdb.set_trace()
        return context

@require_POST
def follow(request, pk):
    user = User.objects.get(id=pk)
    if 'request_follow' in request.POST:
       Friend.objects.add_friend(request.user, user)
    if 'remove_follow' in request.POST:
        Friend.objects.remove_friend(request.user, user)
    if 'not_follow' in request.POST:
        Friend.objects.remove_friend(request.user, user)
    return render(request, 'accounts/follow.html', {'login_user': request.user})

@require_POST
def block(request, pk):
    other_user = User.objects.get(id=pk)
    if 'block' in request.POST:
       Block.objects.add_block(request.user, other_user)
    if 'remove_block' in request.POST:
       Block.objects.remove_block(request.user, other_user)
    return render(request, 'accounts/block.html',{'login_user': request.user})


class Info(LoginRequiredMixin, TemplateView):
    template_name = "accounts/info.html"

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, id=self.kwargs['pk'])
        login_user = self.request.user
        following = Follow.objects.following(user)
        followers = Follow.objects.followers(user)
        friends = Friend.objects.are_friends(login_user, user)
        blocking_user = Block.objects.is_blocked(login_user, user)
        requesting_follows = Friend.objects.sent_requests(user=user)
        requested_follows = Friend.objects.unread_requests(user=user)
        context={
            'user': user,
            'login_user': login_user,
            'following': following,
            'followers': followers,
            'friends': friends,
            'blocking_user': blocking_user,
            'requesting_follows': requesting_follows,
            'requested_follows': requested_follows
        }
        return context

@require_POST
def accept(request, pk):
    user = User.objects.get(id=pk)
    # if 'accept' in request.POST:
        # pdb.set_trace()
    friend_request = FriendshipRequest.objects.get(from_user=pk, to_user=request.user.id)
    friend_request.accept()
    Follow.objects.add_follower(request.user, user)
    return render(request, 'accounts/accept.html',{'login_user': request.user})

@require_POST
def reject(request, pk):
    user = User.objects.get(id=pk)
    friend_request = FriendshipRequest.objects.get(from_user=pk, to_user=request.user.id)
    friend_request.reject()
    Friend.objects.remove_friend(request.user, user)
    return render(request, 'accounts/reject.html', {'login_user': request.user})

class IndexView(ListView):
    model = User
    template_name = "accounts/index.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_user"] = self.request.user
        return context