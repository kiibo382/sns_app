from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
CustomUser = get_user_model()

# class LoginForm(forms.Form):
#     username = UsernameField(
#         label='ユーザー名',
#         max_length=255,
#     )
#
#     password = forms.CharField(
#         label='パスワード',
#         widget=forms.PasswordInput(render_value=True),
#     )
    #
    # class Meta:
    #     model = User
    #     fields = ('username', 'password', 'Queryset')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = field.label


# class UserCreateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#         widgets = {
#             'password': forms.PasswordInput(attrs={'placeholder': 'パスワード'})
#         }
#
#     password2 = forms.CharField(
#         label='確認用パスワード',
#         required=True,
#         widget=forms.PasswordInput(attrs={'placeholder': '確認用パスワード'})
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label