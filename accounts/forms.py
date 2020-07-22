from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
