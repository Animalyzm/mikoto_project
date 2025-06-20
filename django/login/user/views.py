from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm


def home(request):
    return render(request, 'user/home.html', context={})
    

def signup_func(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():  # True or False
            user = signup_form.save(commit=False)  # commit=False の場合のみインスタンスを返す
            password = signup_form.cleaned_data['password']
            user.set_password(password)  # パスワードのハッシュ化
            user.save()
            messages.success(request, 'サインアップに成功しました')
            login(request, user)
            return redirect('user:home')
            # return redirect('/user')
        else:
            messages.error(request, 'サインアップに失敗しました')
            return redirect('user:signup')
    else:
        signup_form = SignupForm()
        return render(request, 'user/signup.html', context={'form': signup_form})
        
        
def login_func(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'ログインしました')
                return redirect('user:home')
            else:
                messages.error(request, 'ログインに失敗しました')
                return redirect('user:login')
        else:
            messages.error(request, 'ログインに失敗しました')
            return redirect('user:login')
    else:
        login_form = LoginForm()
        return render(request, 'user/login.html', context={'form': login_form})


def logout_func(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('user:login')
