from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView

from .forms import PostAddForm
from .models import Post, Tag, Like
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class IndexView(ListView):
    model = Post
    template_name = "twitterclone/index.html"
    paginate_by = 20

index = IndexView.as_view()


class DetailView(DetailView):
    model = Post
    template_name = 'twitterclone/detail.html'

detail = DetailView.as_view()

def post_new(request):
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
   return render(request, 'twitterclone/post_new.html', {'form': form})

class EditView(UpdateView):
    model = Post
    template_name = 'twitterclone/edit.html'
    form_class = PostAddForm
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "保存できませんでした")
        return super().form_invalid(form)

edit = EditView.as_view()

def delete(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   post.delete()
   return redirect('twitterclone:index')

@login_required
def like(request, *args, **kwargs):
    post = Post.objects.get(id=kwargs['pk'])
    is_like = Like.objects.filter(user=request.user).filter(post=post).count()
    # unlike
    if is_like > 0:
        liking = Like.objects.get(post_id=kwargs['pk'], user=request.user)
        liking.delete()
        post.like_num -= 1
        post.save()
        messages.warning(request, 'いいねを取り消しました')
        return redirect(reverse_lazy('twitterclone:detail', kwargs={'pk': kwargs['pk']}))
    # like
    post.like_num += 1
    post.save()
    like = Like()
    like.user = request.user
    like.post = post
    like.save()
    messages.success(request, 'いいね！しました')
    return HttpResponseRedirect(reverse_lazy('twitterclone:detail', kwargs={'pk': kwargs['pk']}))