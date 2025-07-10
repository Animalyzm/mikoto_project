from django.db import models
import markdown
from markdownx.models import MarkdownxField


class Post(models.Model):
    title = models.CharField('タイトル', max_length=64)
    content = MarkdownxField('本文')
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    page_views = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def markdown_to_html(self):
        md = markdown.Markdown(extensions=['extra', 'admonition', 'sane_lists', 'toc'])
        html = md.convert(self.content)
        return html
