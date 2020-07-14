from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from . import forms

class LoginView(AuthLoginView):
    form_class = forms.LoginForm
    template_name = 'accounts/login.html'

login = LoginView.as_view()

class Logout(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"

logout = Logout.as_view()

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/create.html"
    success_url = reverse_lazy("login")

create = UserCreateView.as_view()