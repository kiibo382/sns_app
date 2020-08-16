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
        found = resolve('/accounts/login/')
        self.assertEqual(found.func.view_class, Login)

    def test_url_resolves_to_logout_view(self):
        self.client.login(username='test', password='test')
        found = resolve('/accounts/logout/')
        self.assertEqual(found.func.view_class, Logout)

    def test_url_resolves_to_accounts_create_view(self):
        found = resolve('/accounts/create/')
        self.assertEqual(found.func.view_class, UserCreateView)

    def test_url_resolves_to_user_index_view(self):
        found = resolve('/accounts/index/')
        self.assertEqual(found.func.view_class, IndexView)
