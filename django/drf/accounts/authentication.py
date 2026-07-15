from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTCookieAuthentication(JWTAuthentication):
    """
    Authorization ヘッダが無いとき、HttpOnly の access Cookie を JWT として扱う
    """
    def authenticate(self, request):
        header = self.get_header(request)
        # ヘッダがある場合は、シンプル JWT の認証クラスを使用
        if header is not None:
            return super().authenticate(request)
        
        # ヘッダがない場合は、Cookie のトークンを使用
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            # Cookie のトークンがない場合は、認証を失敗
            return None
        
        # Cookie のトークンを使用して認証
        validated_token = self.get_validated_token(raw_token)
        # 認証が成功した場合は、ユーザーとトークンを返す
        return self.get_user(validated_token), validated_token
