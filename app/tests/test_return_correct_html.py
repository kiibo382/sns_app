import pdb

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from app.models import Post, Tag
from app.views import IndexView, DetailView, EditView, post_new, delete, Likes


class HtmlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(HtmlTests, cls).setUpClass()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        post=Post()
        tag=Tag()
        tag.tag='tag'
        tag.save()
        post.author=user
        post.tag=tag
        post.text='text'
        post.save()

    def test_top_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitterclone/index.html')

    def test_add_post_page_returns_correct_html(self):
        response = self.client.get('/post_new/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test', password='test')
        response=self.client.get('/post_new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitterclone/post_new.html')

        t=Tag()
        t.tag='t'
        t.save()
        self.client.post(reverse('twitterclone:post_new'), data={'text': 'ttt','tag': 1})
        self.assertTrue(Post.objects.get(text='ttt'))

    def test_detail_page_returns_correct_html(self):
        self.client.login(username='test', password='test')
        response=self.client.get('/detail/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitterclone/detail.html')

    def test_edit_page_returns_correct_html(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/edit/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitterclone/edit.html')
        self.client.post('/edit/1/', data={'text': 'ttttt', 'tag': 1})
        self.assertTrue(Post.objects.get(text='ttttt'))

    def test_delete_page_returns_correct_html(self):
        self.client.login(username='test', password='test')
        self.client.get('/delete/1/')
        try:
            post = Post.objects.get(id=1)
        except:
            post=None
        self.assertEqual(post, None)