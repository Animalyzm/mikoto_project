from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

  
class RegisterSerializer(serializers.ModelSerializer):
    """ ユーザー登録シリアライザー """
    # Django 標準のバリデーションを使う
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        ユーザー登録シリアライザーのメタクラス
        ユーザー登録時に使用するフィールドを定義する
        """
        model = User
        fields = ('username', 'password', 'password2', 'email')
    
    def validate(self, attrs):
        """ パスワードの検証 """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "パスワードが一致しません"})
        return attrs

    def create(self, validated_data):
        """ ユーザーの作成 """
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    """ ユーザー情報シリアライザー """
    class Meta:
        """
        ユーザー情報シリアライザーのメタクラス
        ユーザー情報を取得する際に使用するフィールドを定義する
        """
        model = User
        fields = ('id', 'username', 'email')
