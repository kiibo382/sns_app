from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView

from .forms import PostAddForm
from .models import Post, Tag
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy

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

# def edit(request, post_id):
#    post = get_object_or_404(Post, id=post_id)
#    if request.method == "POST":
#        form = PostAddForm(request.POST, instance=post)
#        if form.is_valid():
#            form.save()
#            return redirect('twitterclone:detail', post_id=post.id)
#    else:
#        form = PostAddForm(instance=post)
#    return render(request, 'twitterclone/edit.html', {'form': form, 'post':post })

class EditView(UpdateView):
    model = Post
    template_name = 'twitterclone/edit.html'
    form_class = PostAddForm
    success_url = "/"

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "保存できませんでした")
        return super().form_invalid(form)

edit = EditView.as_view()

def delete(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   post.delete()
   return redirect('twitterclone:index')
