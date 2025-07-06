from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Content(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=64)
    content = models.TextField('コンテンツ', max_length=256)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    
    def __str__(self):
        return self.title


class Check(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    reader = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    writer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField('コメント', max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment[:10]
    
    
class Connect(models.Model):
    connect = models.ForeignKey(get_user_model(), related_name='connect', on_delete=models.CASCADE)
    connected = models.ForeignKey(User, related_name='connected', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.connected.id}:{self.connected}'
    
    
class Good(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    reader = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
