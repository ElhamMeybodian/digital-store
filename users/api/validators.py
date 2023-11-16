import re

from django.core.cache import caches
from django.utils.translation import gettext_lazy as _
from rest_captcha import utils
from rest_captcha.settings import api_settings
from rest_framework import serializers

from digital_store import settings

cache = caches[api_settings.CAPTCHA_CACHE]



def check_difficulty_password(value, difficulty_level):
    difficulty = settings.PASSWORDS_STRENGTH_REGEX
    regex = re.compile(difficulty[difficulty_level].get("regex"))
    return regex.match(value)


def password_difficulty(value):
    message = _('password strength not enough')
    if check_difficulty_password(value, "medium") is None:
        raise serializers.ValidationError(message)
