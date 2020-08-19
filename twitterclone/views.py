from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView
from django.views.generic.base import View
from .forms import PostAddForm
from .models import Post, Tag, Like
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class IndexView(ListView):
    model = Post
    template_name = "twitterclone/index.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_user"] = self.request.user
        return context


class DetailView(DetailView):
    model = Post
    template_name = 'twitterclone/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_user"] = self.request.user
        like_posts = {}
        for post in Post.objects.all():
            like_posts[post.id] = Like.objects.filter(post=post)
        context['like_posts'] = like_posts
        return context


@login_required
def post_new(request):
    login_user = request.user
    if request.method == "POST":
        form = PostAddForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('twitterclone:index')
    else:
        form = PostAddForm()

    return render(request, 'twitterclone/post_new.html', {'form': form, "login_user": login_user})


class EditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'twitterclone/edit.html'
    form_class = PostAddForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_user"] = self.request.user
        return context

    def form_valid(self, form):
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした")
        return super().form_invalid(form)


@login_required
def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('twitterclone:index')


class Likes(View):
    model = Like
    slug_field = 'post'
    slug_url_kwarg = 'postId'

    def get(self, request, postId):
        post = Post.objects.get(id=postId)
        like = Like.objects.filter(user=self.request.user, post=post)
        like_posts = {}
        if like.exists():
            like.delete()
            post.like_num -= 1
            post.save()
        else:
            like = Like(user=self.request.user, post=post)
            post.like_num += 1
            post.save()
            like.save()
        like_posts[post.id] = Like.objects.filter(post=post)
        return render(request, 'twitterclone/like.html', {
            'like_posts': like_posts,
            'post': post
        })
