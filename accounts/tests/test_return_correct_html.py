from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import resolve
from accounts.views import Login, Logout, UserCreateView, Profile, follow,  block, Info, accept, reject, IndexView
import pdb

class UrlResolveTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(UrlResolveTests, cls).setUpClass()
        user=User.objects.create(username='test')
        user.set_password('test')
        user.save()

    def test_url_resolves_to_login_view(self):
        c = Client()
        response = c.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_logout_view(self):
        c=Client()
        response = c.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test', password='test')
        res = self.client.get('/post_new/')
        self.assertEqual(res.status_code, 200)

    def test_url_resolves_to_accounts_create_view(self):
        c = Client()
        response = c.get('/accounts/create/')
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_user_index_view(self):
        c = Client()
        response = c.get('/accounts/index/')
        self.assertEqual(response.status_code, 200)
