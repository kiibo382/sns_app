from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('create/', views.UserCreateView.as_view(),name="create"),
    path('index/', views.IndexView.as_view(), name="index"),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/<int:user_id>/info/', views.info, name='info'),
]