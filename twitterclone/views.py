from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Post


def index(request):
    latest_post_list = Post.objects.order_by('-published_date')[:5]
    context = {'latest_question_list': latest_post_list}
    return render(request, 'index.html', context)
