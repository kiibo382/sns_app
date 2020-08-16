from django.test import TestCase
from django.test.client import Client
from django.urls import resolve
from twitterclone.views import post_new, DetailView, IndexView, EditView, delete, Likes

class UrlResolveTests(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #
    #
    # def setUp(self):

    def test_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, IndexView)

    def test_url_resolves_to_post_add_view(self):
        found = resolve('/post_new/')
        self.assertEqual(found.func, post_new)

    def test_url_resolves_to_post_edit_view(self):
        found = resolve('/edit/1/')
        self.assertEqual(found.func.view_class, EditView)

    def test_url_resolves_to_post_delete_view(self):
        found = resolve('/delete/1/')
        self.assertEqual(found.func, delete)

    def test_url_resolves_to_post_detail_view(self):
        found = resolve('/detail/1/')
        self.assertEqual(found.func.view_class, DetailView)