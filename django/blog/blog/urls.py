from django.conf import settings  # 追加
from django.conf.urls.static import static  # 追加
from django.contrib import admin
from django.urls import path, include  # 変更


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),  # 追加
    path('markdownx/', include('markdownx.urls')),  # 追加
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 開発用 # 追加
