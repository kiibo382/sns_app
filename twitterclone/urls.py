from django.urls import path
from . import views

app_name = 'twitterclone'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('post_new/', views.post_new, name='post_new'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    # path('follow/<int:pk>/', views.follow, name='follow'),
]