from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserTest(APITestCase):

    def setUp(self):
        self.some_user = User.objects.create(email="some_user@email.com", username="some_user")

    def test_user_create(self):
        """Тестирование создания пользователя"""

        url = reverse("users:register")
        data = {"email": "testuser@email.com", "username": "testuser", "password": 12345}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_retrieve(self):
        """Тестирование детального отображения профиля"""
        self.client.force_authenticate(user=self.some_user)
        url = reverse("users:profile", args=(self.some_user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("last_name"), self.some_user.last_name)

    def test_user_update(self):
        """Тестирование обновление профиля пользователя"""

        self.client.force_authenticate(user=self.some_user)
        url = reverse("users:profile-update", args=(self.some_user.pk,))
        data = {"last_name": "Ivanov", "first_name": "Ivan"}
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('last_name'), 'Ivanov')

    def test_user_delete(self):
        """Тестирование удаления пользователя"""

        self.client.force_authenticate(user=self.some_user)
        url = reverse("users:profile-delete", args=(self.some_user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
