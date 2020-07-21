from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import render,  get_object_or_404
from friendship.models import Friend, Follow, Block, FriendshipRequest


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
    user = get_object_or_404(User, pk=user_id)
    posts = user.post_set.all().order_by('-published_date')
    if request.method == 'POST':
       if 'request-follow' in request.POST:
           other_user = User.objects.get(pk=user_id)
           Friend.objects.add_friend(
               request.user,  # The sender
               other_user,  # The recipient
               message='Hi! I would like to add you')

    if request.method == 'POST':
        if 'remove-follow' in request.POST:
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

    follwers = Follow.objects.followers(user)
    followings = Follow.objects.following(user)
    other_user = User.objects.get(pk=user_id)
    friends=Friend.objects.are_friends(request.user, other_user)
    blocking_user = Block.objects.is_blocked(request.user, other_user)
    request_follow = Friend.objects.sent_requests(user)
    requested_follow = Friend.objects.unread_requests(user)
    if request.method == 'POST':
        if 'accept' in request.POST:
            friend_request = FriendshipRequest.objects.get(to_user=requested_follow.id)
            friend_request.accept()

    return render(request, 'accounts/profile.html',
                 {'user': user,
                  'posts': posts,
                  'followers': follwers,
                  'followings': followings,
                  'blocking_user': blocking_user,
                  'friends': friends,
                  'requesting-follow': request_follow,
                  'requested-follow': requested_follow
                  }
                 )

class IndexView(ListView):
    model = User
    template_name = "accounts/index.html"
    paginate_by = 20

def index(request):
    followings_count = Follow.objects.following(request.user).count()
    followers_count = Follow.objects.followers(request.user).count()
    render({'followings_count': followings_count,
            'followers_counts': followers_count})