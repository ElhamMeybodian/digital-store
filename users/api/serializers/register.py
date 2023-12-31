import random

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import PasswordField

from users.api.validators import password_difficulty


class UserCreateSerializer(serializers.ModelSerializer):
    password = PasswordField(validators=[password_difficulty])
    confirm_password = PasswordField()
    code = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password',
            'confirm_password',
            'email',
            'phone_number',
            'code',
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            'username': {'required': True},
            'phone_number': {'required': True},
            'email': {'required': True},
            'code': {"read_only": True},
        }

    def get_code(self, obj):
        code = random.randint(10000, 99999)
        cache.set(str(obj.phone_number), code, 300)
        return code

    def validate_username(self, value):
        if value in get_user_model().objects.filter(username=value).values_list("username", flat=True):
            raise ValidationError({"username": _("username is duplicate")})
        return value

    def validate_phone_number(self, value):
        if value in get_user_model().objects.filter(phone_number=value).values_list("phone_number", flat=True):
            raise ValidationError({"phone_number": _("phone_number is duplicate")})
        return value

    def validate_confirm_password(self, value):
        if self.get_initial().get('password') != value:
            raise ValidationError({"confirm_password": _("The password does not match")})
        return value

    def validate_password(self, value):
        data = self.initial_data.copy()
        data.pop('confirm_password')
        try:
            validate_password(password=data['password'])
        except ValidationError as err:
            raise ValidationError({"password": str(err)})
        return value

    def to_representation(self, instance):
        code = self.get_code(instance)
        data = {
            "code": code,
        }
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = get_user_model().objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        # subject = 'Activate Account'
        # message = f'Hi {user.username}, thank you for registering in DIGITAL STORE.' \
        #           f'{code}'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email, ]
        # user.email_user(subject, message, email_from, recipient_list)
        # validated_data['message'] = "Please confirm your email address to complete the registration"
        return user


class ActivateAccountSerializer(serializers.Serializer):
    activate_code = serializers.IntegerField(required=True)

    def validate_activate_code(self, value):
        if cache.get(str(self.instance.phone_number)) == value:
            return value
        raise ValidationError({"activate_code": _("activate_code is wrong")})


