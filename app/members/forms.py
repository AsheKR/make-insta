from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 존재하는 사용자입니다.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('비밀번호 두 값이 같지 않습니다.')

    def save(self):
        if self.errors:
            raise ValueError('폼 데이터 유효성 검사에 실패했습니다')
        return User.objects.create_user(username=self.cleaned_data.get('username'),
                                        password=self.cleaned_data.get('password1'))


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'img_profile',
            'site',
            'introduce',
        ]