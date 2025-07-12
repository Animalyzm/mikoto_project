from .models import Category


def category_list(request):
    """ テンプレートに毎回渡すデータ
    settings.py: TEMPLATES...OPTIONSの設定必要
    "
    context = {
        'category_list': Category.objects.all(),
    }
    return context
