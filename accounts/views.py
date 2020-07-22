from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import render,  get_object_or_404
from friendship.models import Friend, Follow, Block, FriendshipRequest
from .forms import ProfileForm


class Login(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"
login = Login.as_view()

class Logout(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/create.html"
    success_url = reverse_lazy('accounts:login')

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = user.post_set.all().order_by('-published_date')
    if request.method == 'POST':
       if 'request_follow' in request.POST:
           other_user = User.objects.get(pk=user_id)
           Friend.objects.add_friend(
               request.user,  # The sender
               other_user,  # The recipient
            )

    if request.method == 'POST':
        if 'remove_follow' in request.POST:
            other_user = User.objects.get(pk=user_id)
            Friend.objects.remove_friend(request.user, other_user)

    if request.method == 'POST':
        if 'block' in request.POST:
           other_user = User.objects.get(pk=user_id)
           Block.objects.add_block(request.user, other_user)

    if request.method == 'POST':
        if 'remove_block' in request.POST:
           other_user = User.objects.get(pk=user_id)
           Block.objects.remove_block(request.user, other_user)

    followings = Follow.objects.following(user)
    followers = Follow.objects.followers(user)
    other_user = User.objects.get(id=user_id)
    friends = Friend.objects.are_friends(request.user, other_user)
    blocking_user = Block.objects.is_blocked(request.user, other_user)
    requesting_follows = Friend.objects.sent_requests(user=user)
    requested_follows = Friend.objects.unread_requests(user=user)
    like_posts = user.like_user.all()
    for requested_follow in requested_follows:
        ed_follow=requested_follow.from_user
        if Friend.objects.are_friends(ed_follow, other_user)==True:
            requested_follows.remove(requested_follow)

    for requesting_follow in requesting_follows:
        ing_follow=requesting_follow.to_user
        if Friend.objects.are_friends(ing_follow, other_user) == True:
            requesting_follows.remove(requesting_follow)

    if request.method == 'POST':
        if 'accept' in request.POST:
            friend_request = FriendshipRequest.objects.get(to_user=request.POST.get('ed_follow').id)
            friend_request.accept()
            Follow.objects.add_follower(request.user, request.POST.get('ed_follow'))

    if request.method == 'POST':
        if 'reject' in request.POST:
            friend_request = FriendshipRequest.objects.get(to_user=request.POST.get('ed_follow'))
            friend_request.reject()

    return render(request, 'accounts/profile.html',
                 {'user': user,
                  'posts': posts,
                  'followings': followings,
                  'followers': followers,
                  'blocking_user': blocking_user,
                  'friends': friends,
                  'requesting_follows': requesting_follows,
                  'requested_follows': requested_follows,
                  'like_posts': like_posts,
                  }
                 )

class IndexView(ListView):
    model = User
    template_name = "accounts/index.html"
    paginate_by = 20