from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Profile, Device, User


class UserRegisterTest(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.url_register = reverse("users:register")
        self.url_activate = reverse("users:activate-user", kwargs={"username": self.username})
        self.payload = {
            'username': self.username,
            'email': "test@gmail.com",
            'phone_number': '989912345678',
            'password': "@@Test%%%%123",
            'confirm_password': "@@Test%%%%123",
            'first_name': "test",
            'last_name': "testian",
        }

    def test_register_user_successful(self):
        response = self.client.post(self.url_register, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, User.objects.filter(username=self.username).count())
        self.assertFalse(User.objects.get(username=self.username).is_active)
        self.assertEqual(0, Profile.objects.filter(user__username=self.username).count())
        self.assertEqual(0, Device.objects.filter(user__username=self.username).count())
        data = {
            "activate_code": response.data.get('code')
        }
        response = self.client.post(self.url_activate, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.get(username=self.username).is_active)
        self.assertEqual(1, Profile.objects.filter(user__username=self.username).count())
        self.assertEqual(1, Device.objects.filter(user__username=self.username).count())
