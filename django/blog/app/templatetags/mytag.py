from django import template


register = template.Library()  # タグやフィルター登録の初期化処理

@register.simple_tag
def url_replace(request, key, value):
    url_dict = request.GET.copy()
    print(url_dict, key, value)
    url_dict[key] = value
    return url_dict.urlencode()
