import pdb

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import QuerySet

from twitterclone.models import Post, Tag, Like
from django.test import TestCase, RequestFactory
from twitterclone.views import Likes

class SaveLikeRequestTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SaveLikeRequestTests, cls).setUpClass()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()

    def test_like_save(self):
        self.client.login(username='test', password='test')
        user = User.objects.get(username='test')
        other_user = User.objects.create_user(username='hoge', password='hoge')
        tag = Tag()
        tag.tag = 'tag'
        tag.save()
        post = Post()
        post.author = other_user
        post.text = 'text'
        post.tag = tag
        post.save()
        rf=RequestFactory()
        request = rf.get("/1/like/")
        request.user=user
        res=Likes.as_view()(request, post.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Like.objects.filter(user=request.user, post=post).exists())
        rf.get("/1/like/")
        request.user = user
        res = Likes.as_view()(request, post.id)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Like.objects.filter(user=request.user, post=post).exists())
