from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie


from .forms import SignupForm, LoginForm, PostsForm, CommentForm, SearchForm
from .models import Content, Check, Comment, Connect, Good


PAGENATOR_NUM = 3


def index(request):
    user_id = request.user.id
    connects = Connect.objects.filter(connect=request.user.id)
    author_id_list = [connect.connected for connect in connects]
    author_id_list.append(user_id)
    user_objects = Content.objects.order_by('-created_at').filter(author_id__in=author_id_list)
    paginator = Paginator(user_objects, PAGENATOR_NUM)
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
    paginator = Paginator(objs, PAGENATOR_NUM)
    page_number = request.GET.get('page')
    context = {
        'page_obj': paginator.get_page(page_number),
        'page_number': page_number,
        'title': 'ホーム',
    }
    return render(request, 'text_sns/index.html', context)


def check_func(request, content_id):
    reader = request.user
    content = Content.objects.get(pk=content_id)
    exists = Check.objects.filter(content=content, reader=reader).exists()
    if not exists:
        check = Check.objects.create(content=content, reader=reader)
        check.save()
        messages.warning(request, 'チェックしました')
    else:
        check = Check.objects.get(content=content, reader=reader)
        check.delete()
        messages.success(request, 'チェックを外しました')
    return redirect('text_sns:check_contents')


def check_contents_func(request):
    check_objs= Check.objects.filter(reader=request.user).all()
    check_content_id_list = [obj.content_id for obj in check_objs]
    check_content_objs = Content.objects.filter(id__in=check_content_id_list).order_by('-created_at')
    paginator = Paginator(check_content_objs, PAGENATOR_NUM)
    page_number = request.GET.get('page')
    context = {
        'page_obj': paginator.get_page(page_number),
        'page_number': page_number,
        'title': 'チェック一覧',
    }
    return render(request, 'text_sns/index.html', context)


def comment_func(request, content_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            messages.error(request, 'コメントしました')
            return redirect('text_sns:index')
        else:
            messages.error(request, 'コメントできませんでした')
            return redirect('text_sns:index')
    else:
        comment_form = CommentForm()
        context={
            'form': comment_form,
            'content_id': content_id,
        }
        return render(request, 'text_sns/comment.html', context)


def comment_delete_func(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    messages.error(request, 'コメントを削除しました')
    return redirect('text_sns:index')


def connect_func(request, content_id):
    author_id = Content.objects.get(pk=content_id).author_id
    user = request.user
    if user.id == author_id:
        messages.warning(request, '自分とはつながれません')
        return redirect('text_sns:index')
    author = User.objects.get(pk=author_id)
    connects = Connect.objects.filter(connect=user.id)
    if Connect.objects.filter(connect=user.id, connected=author_id).exists():
        messages.warning(request, '{}さんとは、すでにつながっています'.format(author.username))   
    else:
        connect = Connect.objects.create(connect=user, connected=author)
        connect.save()
        messages.warning(request, '{}さんと、つながりました'.format(author.username))  
    connects = Connect.objects.filter(connect=user.id)
    return render(request, 'text_sns/connects.html', context={'connects': connects})


def connects_func(request):
    connects = Connect.objects.filter(connect=request.user.id)
    return render(request, 'text_sns/connects.html', context={'connects': connects})


def connect_seeyou_func(request, connected_id):
    connect = Connect.objects.filter(connect=request.user.id, connected=connected_id)
    connect.delete()
    connected = User.objects.get(pk=connected_id)
    messages.success(request, '{}さんと、またねしました'.format(connected.username))
    connects = Connect.objects.filter(connect=request.user.id)
    return render(request, 'text_sns/connects.html', context = {'connects': connects})


@ensure_csrf_cookie
def good_func(request, content_id):
    d = {"message": "error"}
    if request.method == 'POST':
        reader = request.user
        content = Content.objects.get(pk=content_id)
        exists = Good.objects.filter(content=content, reader=reader).exists()
        if not exists:
            good = Good.objects.create(content=content, reader=reader)
            good.save()
            d = {"message": "create"}
        else:
            good = Good.objects.get(content=content, reader=reader)
            good.delete()
            d = {"message": "delete"}
    return JsonResponse(d)


def search_func(request):
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)
        if searchForm.is_valid():
            keyword = searchForm.cleaned_data['keyword']
            object_list = Content.objects.filter(Q(author__username__icontains=keyword) | 
                                                 Q(title__icontains=keyword) |
                                                 Q(content__icontains=keyword))
            paginator = Paginator(object_list, PAGENATOR_NUM)
            page_number = request.GET.get('page')
            context = {
                'page_obj': paginator.get_page(page_number),
                'page_number': page_number,
                'title': f'キーワード: {keyword} 検索結果',
            }
            return render(request, 'text_sns/index.html', context)
        else:
            messages.error('検索内容を変更してください')
            searchForm = SearchForm() 
            return render(request, 'text_sns/search.html', context)
    else:
        searchForm = SearchForm() 
        context={'form': searchForm}
    return render(request, 'text_sns/search.html', context)
