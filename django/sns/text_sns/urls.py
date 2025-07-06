from django.urls import path

from . import views


app_name = 'text_sns'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_func, name='signup'),
    path('login/', views.login_func, name='login'),
    path('logout/', views.logout_func, name='logout'),
    path('delete_confirm/', views.delete_confirm_func, name='delete_confirm'),
    path('user_delete/', views.user_delete_func, name='user_delete'),
    path('posts/', views.posts_func, name='posts'),
    path('posts_delete/<int:content_id>/', views.posts_delete_func, name='posts_delete'),
    path('all_contents', views.all_contents_func, name='all_contents'),
    path('check/<int:content_id>/', views.check_func, name='check'),
    path('check_contents/', views.check_contents_func, name='check_contents'),
    path('comment/<int:content_id>/', views.comment_func, name='comment'),
    path('comment_delete/<int:comment_id>/', views.comment_delete_func, name='comment_delete'),
    path('connect/<int:content_id>/', views.connect_func, name='connect'),
    path('connects/', views.connects_func, name='connects'),
    path('connect_seeyou/<int:connected_id>/', views.connect_seeyou_func, name='connect_seeyou'),
    path('good/<int:content_id>/', views.good_func, name='good'),
    path('search/', views.search_func, name='search'),
]
