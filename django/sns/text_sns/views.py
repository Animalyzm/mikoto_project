from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm, PostsForm
from .models import Content


PAGENATOR_NUM = 3


def index(request):
    objs = Content.objects.filter(author=request.user.id).order_by('-created_at')
    paginator = Paginator(objs, PAGENATOR_NUM)
    page_number = request.GET.get('page')
    context = {
        'page_obj': paginator.get_page(page_number),
        'page_number': page_number,
        'title': 'ホーム',
    }
    return render(request, 'text_sns/index.html', context)


def signup_func(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():  # True or False
            user = signup_form.save(commit=False)  # commit=False のみインスタンスを返す
            password = signup_form.cleaned_data['password']
            user.set_password(password)  # パスワードのハッシュ化
            user.save()
            messages.success(request, 'サインアップに成功しました')
            login(request, user)
            return redirect('text_sns:index')
        else:
            messages.error(request, 'サインアップに失敗しました')
            return redirect('text_sns:signup')
    else:
        signup_form = SignupForm()
        return render(request, 'text_sns/signup.html', context={'form': signup_form},)
        
        
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
                return redirect('text_sns:index')
            else:
                messages.error(request, 'ログインに失敗しました')
                return redirect('text_sns:login')
        else:
            messages.error(request, 'ログインに失敗しました')
            return redirect('text_sns:login')
    else:
        login_form = LoginForm()
        return render(request, 'text_sns/login.html', context={'form': login_form})


def logout_func(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('text_sns:login')


def delete_confirm_func(request):
    return render(request, 'text_sns/delete_confirm.html', context={})
    
    
def user_delete_func(request):
    user = str(request.user)
    if user != 'AnonymousUser':
        user = User.objects.filter(pk=request.user.id)
        user.delete()
        return render(request, 'text_sns/user_delete.html', context={})
    else:
        return redirect('text_sns:index')
    
    
def posts_func(request):
    if request.method == 'POST':
        posts_form = PostsForm(request.POST)
        if posts_form.is_valid():
            posts_form.save()
        return redirect('text_sns:index')
    else:
        posts_form = PostsForm()
        return render(request, 'text_sns/posts.html', context={'form': posts_form})
    
    
def posts_delete_func(request, content_id):
    content = Content.objects.get(pk=content_id)
    content.delete()
    messages.success(request, 'コンテンツを削除しました')
    return redirect('text_sns:index')


def all_contents_func(request):
    objs = Content.objects.all().order_by('-created_at')
    context = {
        'objs': objs
    }
    return render(request, 'text_sns/index.html', context)
