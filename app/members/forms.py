from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def clean(self):
        super().clean()
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user is None:
            raise forms.ValidationError('해당 사용자가 없습니다.')
        self._user = user

    @property
    def user(self):
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패하였습니다.')
        return self._user