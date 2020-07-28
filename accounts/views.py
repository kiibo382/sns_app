from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import render,  get_object_or_404
from friendship.models import Friend, Follow, Block, FriendshipRequest

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

    def get(self, request, *args, **kwargs):
        user = self.request.user
        posts= user.post_set.all().order_by('-published_date')
        friends = Friend.objects.are_friends(request.user, self.request.user)
        blocking_user = Block.objects.is_blocked(request.user, self.request.user)
        like_posts = user.like_user.all()
        requesting_follows = Friend.objects.sent_requests(user=request.user)
        context = {'friends': friends,
                   'blocking_user': blocking_user,
                   'like_posts': like_posts,
                   'requesting_follows': requesting_follows}
        return self.render_to_response(context)

    def post(self, request):
        if 'request_follow' in request.POST:
           Friend.objects.add_friend(request.user, self.request.user)
        if 'remove_follow' in request.POST:
            Friend.objects.remove_friend(request.user, self.request.user)
        if 'block' in request.POST:
           Block.objects.add_block(request.user, self.request.user)
        if 'remove_block' in request.POST:
           Block.objects.remove_block(request.user, self.request.user)

# def profile(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     posts = user.post_set.all().order_by('-published_date')
#     other_user = User.objects.get(id=user_id)
#     friends = Friend.objects.are_friends(request.user, other_user)
#     blocking_user = Block.objects.is_blocked(request.user, other_user)
#     like_posts = user.like_user.all()
#     requesting_follows = Friend.objects.sent_requests(user=request.user)
#     if request.method == 'POST':
#         if 'request_follow' in request.POST:
#            Friend.objects.add_friend(request.user, other_user)
#         if 'remove_follow' in request.POST:
#             Friend.objects.remove_friend(request.user, other_user)
#         if 'block' in request.POST:
#            Block.objects.add_block(request.user, other_user)
#         if 'remove_block' in request.POST:
#            Block.objects.remove_block(request.user, other_user)
#
#     return render(request, 'accounts/profile.html',
#                  {'user': user, 'posts': posts,
#                   'friends': friends,
#                   'blocking_user': blocking_user,
#                   'like_posts': like_posts,
#                   'requesting_follows': requesting_follows})



def info(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = Follow.objects.following(user)
    followers = Follow.objects.followers(user)
    other_user = User.objects.get(id=user_id)
    friends = Friend.objects.are_friends(request.user, other_user)
    requesting_follows = Friend.objects.sent_requests(user=user)
    requested_follows = Friend.objects.unread_requests(user=user)
    blocking_user = Block.objects.is_blocked(request.user, other_user)
    if request.method == 'POST':
        if 'accept' in request.POST:
            friend_request = FriendshipRequest.objects.get(to_user=request.POST.get('ed_follow').id)
            friend_request.accept()
            Follow.objects.add_follower(request.user, request.POST.get('ed_follow'))
        if 'reject' in request.POST:
            friend_request = FriendshipRequest.objects.get(to_user=request.POST.get('ed_follow'))
            friend_request.reject()
            Friend.objects.remove_friend(request.user, request.POST.get('ed_follow'))

    for requested_follow in requested_follows:
        ed_follow=requested_follow.from_user
        if Friend.objects.are_friends(ed_follow, other_user)==True:
            requested_follows.remove(requested_follow)

    for requesting_follow in requesting_follows:
        ing_follow=requesting_follow.to_user
        if Friend.objects.are_friends(ing_follow, other_user) == True:
            requesting_follows.remove(requesting_follow)

    return render(request, 'accounts/info.html',
                  {'user': user,
                   'following': following,
                   'followers': followers,
                   'blocking_user': blocking_user})

class IndexView(ListView):
    model = User
    template_name = "accounts/index.html"
    paginate_by = 20