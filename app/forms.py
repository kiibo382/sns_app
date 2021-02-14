from django import forms
from .models import Post, Tag

class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'tag',)