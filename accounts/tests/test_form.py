from django.contrib.auth.models import User
from django.test import TestCase
from accounts.forms import LoginForm

class LoginFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(LoginFormTests, cls).setUpClass()
        user = User.objects.create(username='test_account')
        user.set_password('test_pass')
        user.save()
    def test_valid(self):
        params = {
            'username': 'test_account',
            'password': 'test_pass'
        }
        form = LoginForm(data=params)
        self.assertTrue(form.is_valid())

    def test_pass_not_valid(self):
        params = {
            'username': 'test_account',
            'password': 'error'
        }
        form = LoginForm(data=params)
        self.assertFalse(form.is_valid())

    def test_name_not_valid(self):
        params = {
            'username': 'error',
            'password': 'test_pass'
        }
        form = LoginForm(data=params)
        self.assertFalse(form.is_valid())