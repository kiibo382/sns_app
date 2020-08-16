import pdb
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from twitterclone.forms import PostAddForm
from twitterclone.models import Post, Tag
from django.test import TestCase

class PostAddFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PostAddFormTests, cls).setUpClass()
        user = User.objects.create(username='test_account')
        user.set_password('test_pass')
        user.save()
        tag=Tag()
        tag.tag='test_tag'
        tag.save()

    def test_valid(self):
        user=authenticate(username='test_account', password='test_pass')
        post=Post()
        post.author=user
        params = {
            'text': 'test_text',
            'tag': 1
        }
        form = PostAddForm(data=params,instance=post)
        self.assertTrue(form.is_valid())

    def test_text_not_valid(self):
        user=authenticate(username='test_account', password='test_pass')
        post=Post()
        post.author=user
        params = {
            'tag': 1
        }
        form = PostAddForm(data=params,instance=post)
        self.assertFalse(form.is_valid())

    def test_tag_not_valid(self):
        user=authenticate(username='test_account', password='test_pass')
        post=Post()
        post.author=user
        params = {
            'text': 'test_text'
        }
        form = PostAddForm(data=params,instance=post)
        self.assertFalse(form.is_valid())
