from django.urls import path
from . import views

app_name = 'twitterclone'
urlpatterns = [
    path('', views.index, name='index'),
]