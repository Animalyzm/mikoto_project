from django.contrib.auth import get_user_model
from django.db import models


class Content(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=64)
    content = models.TextField('コンテンツ', max_length=256)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    
    def __str__(self):
        return self.title
