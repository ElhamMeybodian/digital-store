from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class LoginBaseSerializer(TokenObtainSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['phone_number'] = serializers.IntegerField()
        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = PasswordField()

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['username'] = user.username
        token['phone_number'] = user.phone_number
        token['email'] = user.email
        return token


class LoginSerializer(LoginBaseSerializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)
        refresh = self.get_token(self.user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        return attrs
