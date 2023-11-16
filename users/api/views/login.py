from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework_simplejwt.views import TokenViewBase

from users.api.serializers.login import LoginSerializer


class LoginApiView(TokenViewBase):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except exceptions.AuthenticationFailed as e:
            raise exceptions.ValidationError(_("username or password is wrong"))
