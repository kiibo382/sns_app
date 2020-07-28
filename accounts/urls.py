from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('create/', views.UserCreateView.as_view(),name="create"),
    path('index/', views.IndexView.as_view(), name="index"),
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('profile/<int:pk>/info/', views.Info.as_view(), name='info'),
]