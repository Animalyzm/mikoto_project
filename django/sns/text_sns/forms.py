from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Content


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'password': 'パスワード',
        }
        widgets = {'password': forms.PasswordInput()}
        
    reconfirmation_password = forms.CharField(
        label='パスワード再確認',
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        reconfirmation_password = cleaned_data['reconfirmation_password']
        if password != reconfirmation_password:
            self.add_error('password', 'パスワードが一致しません')
        try:
            validate_password(password, self.instance)  # instance: 入力ユーザー情報
        except ValidationError as e:
            self.add_error('password', e)
        return cleaned_data
    
    
class LoginForm(forms.Form):
    username = forms.CharField(label="ユーザー名")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    
    
class PostsForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('author', 'title', 'content')
        widgets = {
            'author': forms.TextInput(),
            'content': forms.Textarea(attrs={'rows': 6, 'cols': 40}),
        }
    