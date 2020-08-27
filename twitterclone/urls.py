from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'twitterclone'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('post_new/', views.post_new, name='post_new'),
    path('edit/<int:pk>/', views.EditView.as_view(), name='edit'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    path('<postId>/like/', login_required(views.Likes.as_view()),name='like'),
]