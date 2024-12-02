from rest_framework.test import APITestCase
from wallet.factories import UserFactory
from rest_framework import status
from wallet.models import User
from django.contrib.auth.hashers import check_password

class UserTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = '/api/v1/users/'


    def test_user_registration(self):
        self.client.logout()
        data = {
            "username": "test_user_1",
            "password": "12345",
            "email": "test_user_1@gmail.com",
            "first_name": "John",
            "last_name": "Smith",
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.last()

        self.assertTrue(check_password(data['password'] , created_user.password))
        data.pop('password')

        user_data = {
            "username": created_user.username,
            "email": created_user.email,
            "first_name": created_user.first_name,
            "last_name": created_user.last_name,
        }

        self.assertDictEqual(data, user_data)

    def test_try_to_pass_existing_username(self):
        self.client.logout()
        data = {
            "username": self.user.username,
            "password": "12345",
            "email": "test_user_1@gmail.com",
            "first_name": "John",
            "last_name": "Smith",
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 1)