from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """ ユーザー登録ビュー """
    # 誰でもアクセスできるようにする
    permission_classes = (AllowAny,)
    # ユーザー登録シリアライザーを使用する
    serializer_class = RegisterSerializer


class UserDetailView(APIView):
    """ ユーザー情報ビュー """
    # 認証が必要なビュー
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ ユーザー情報を取得 """
        # ユーザー情報をシリアライズして返す
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    ログインビュー
    JWT トークンを HttpOnly な Cookie にセットする
    """
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            access = data.pop('access')
            refresh = data.pop('refresh')

            response.set_cookie(
                key='access_token',
                value=access,
                httponly=True,
                secure=not settings.DEBUG,   # 本番は True
                samesite='Lax',  # 'None',
                max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                path='/',  # サイト全体で有効
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',  # 'None',
                max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                path='/accounts/token_refresh/',  # リフレッシュ用のパス
            )
            # ボディにはトークンを返さない（漏洩防止）
            response.data = {'detail': 'ログインしました'}
        else:
            response.data = {'detail': response.data.get('detail', 'ログインに失敗しました')}
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    """
    リフレッシュビュー
    JWT トークンを HttpOnly な Cookie にセットする
    """
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh_token')
        if refresh:
            request.data._mutable = True  # QueryDict の場合
            request.data['refresh'] = refresh
        return super().post(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            access = response.data.pop('access')
            response.set_cookie(
                key='access_token',
                value=access,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',  # 'None',
                max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                path='/accounts/token_refresh/',  # リフレッシュ用のパス
            )
            # ROTATE_REFRESH_TOKENS=True のとき refresh も返る
            if 'refresh' in response.data:
                refresh = response.data.pop('refresh')
                response.set_cookie(
                    key='refresh_token',
                    value=refresh,
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite='Lax',
                    max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                )
            response.data = {'detail': 'トークンをリフレッシュしました'}
        return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):
    """ ログアウトビュー（Cookie のトークンを削除） """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response({'detail': 'ログアウトしました'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    