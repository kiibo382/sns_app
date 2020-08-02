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
        user = get_object_or_404(User, id=self.kwargs['pk'])
        login_user = self.request.user
        posts = user.post_set.all().order_by('-published_date')
        friends = Friend.objects.are_friends(login_user, user)
        following = Follow.objects.following(login_user)
        blocking_user = Block.objects.is_blocked(login_user, user)
        like_posts = user.like_user.all()
        try:
            requesting_follows = FriendshipRequest.objects.get(to_user=user.id, from_user=login_user.id)
        except:
            pass

        context = {'user': user,
                   'login_user': login_user,
                   'posts': posts,
                   'friends': friends,
                   'following': following,
                   'blocking_user': blocking_user,
                   'like_posts': like_posts,
                   }
        try:
            context['requesting_follows'] = requesting_follows
        except:
            pass
        # pdb.set_trace()
        return context

def follow(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        if 'request_follow' in request.POST:
           Friend.objects.add_friend(request.user, user)
        if 'remove_follow' in request.POST:
            Friend.objects.remove_friend(request.user, user)
        if 'not_follow' in request.POST:
            Friend.objects.remove_friend(request.user, user)
    return render(request, 'accounts/follow.html', {'login_user': request.user})

def block(request, pk):
    other_user = User.objects.get(id=pk)
    if request.method == 'POST':
        if 'block' in request.POST:
           Block.objects.add_block(request.user, other_user)
        if 'remove_block' in request.POST:
           Block.objects.remove_block(request.user, other_user)
    return render(request, 'accounts/block.html',{'login_user': request.user})


class Info(TemplateView):
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
        try:
            requesting_follows = FriendshipRequest.objects.get(to_user=user.id, from_user=login_user.id)
        except:
            pass
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

def accept(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        if 'accept' in request.POST:
            # pdb.set_trace()
            friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=pk)
            friend_request.accept()
            Follow.objects.add_follower(request.user, user)
        return render(request, 'accounts/accept.html',{'login_user': request.user})

def reject(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        if 'reject' in request.POST:
            friend_request = FriendshipRequest.objects.get(from_user=request.user,to_user=pk)
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