from django.urls import path

from . import views


app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('category/<int:category_pk>/', views.CategoryView.as_view(), name='category'),
    path('comment/<int:post_pk>', views.CommentView.as_view(), name='comment'),
]