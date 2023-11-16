import random

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers.register import UserCreateSerializer, ActivateAccountSerializer
from users.models import User


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = get_user_model().objects.all()


class ActivateAccountView(APIView):
    serializer_class = ActivateAccountSerializer

    def post(self, request, *args, **kwargs):
        username = kwargs.get("username", None)
        user = get_object_or_404(User, username=username)
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class SendAgainActivateCodeView(APIView):
    def post(self, request, *args, **kwargs):
        username = kwargs.get("username", None)
        user = get_object_or_404(User, username=username)
        code = random.randint(10000, 99999)
        cache.set(str(user.phone_number), code, 120)
        # send Email
        return Response({'code': code}, status=status.HTTP_200_OK)
