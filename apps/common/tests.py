from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User

# Create your tests here.


class LoginAPITestCase(APITestCase):
    url = reverse("accounts:auth-login")

    def setUp(self):
        self.nip = "11111"
        self.email = "test2@apps.com"
        self.password = "Delvika6"
        self.user = User.objects.create_user(self.nip, self.email, self.password)

    def test_login_valid(self):
        data = {"nip": self.nip, "password": self.password}
        response = self.client.post(self.url, data, format="json")
        expect = {
            "nip": "11111",
            "email": "test2@apps.com",
            "token": {
                "access": response.data["token"]["access"],
                "refresh": response.data["token"]["refresh"],
                "life_time": 900,
            },
        }
        self.assertEqual(response.data, expect)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nip_invalid(self):
        data = {"nip": "username_invalid", "password": self.password}

        response = self.client.post(self.url, data, format="json")

        expect = {
            "success": False,
            "message": "incorrect data",
            "data": {"non_field_errors": ["Unable to login with provided credentials"]},
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expect)

    def test_password_invalid(self):
        data = {"nip": self.nip, "password": "password_invalid"}

        response = self.client.post(self.url, data, format="json")

        expect = {
            "success": False,
            "message": "incorrect data",
            "data": {"non_field_errors": ["Unable to login with provided credentials"]},
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expect)
