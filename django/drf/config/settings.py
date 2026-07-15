from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-os#0h+f@vo33psyrrb4n+vp&lnx7zf13cps8^ql7tp)$mj18h*'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt', 
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = 'static/'


REST_FRAMEWORK = {
    # 認証
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # アカウント･アプリの認証クラス
        'accounts.authentication.JWTCookieAuthentication', 
        # シンプル JWT の認証クラス
        'rest_framework_simplejwt.authentication.JWTAuthentication', 
    ),
    # レンダラー
    # 'DEFAULT_RENDERER_CLASSES': (
        # 本番環境では、JSON形式でレスポンスを返す
        # 'rest_framework.renderers.JSONRenderer',
    # ),
}

# JWTの有効期限を設定するためにインポート
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # アクセストークンの有効期限
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # リフレッシュトークンの有効期限
    'ROTATE_REFRESH_TOKENS': True,  # リフレッシュトークンの更新
    'UPDATE_LAST_LOGIN': True,  # ログイン時に最終ログイン時間を更新
    'AUTH_HEADER_TYPES': ('Bearer',),  # 認証ヘッダーのタイプ
}
