from django.db import models
import markdown
from markdownx.models import MarkdownxField


class Category(models.Model):
    category_name = models.CharField('カテゴリ名', max_length=32)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    
    def __str__(self):
        return self.category_name
    

class Post(models.Model):
    title = models.CharField('タイトル', max_length=64)
    content = MarkdownxField('本文')
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    page_views = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(Category, verbose_name='カテゴリ', blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.title
    
    def markdown_to_html(self):
        md = markdown.Markdown(extensions=['extra', 'admonition', 'sane_lists', 'toc'])
        html = md.convert(self.content)
        return html
