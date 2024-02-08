from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.urls import resolve


class UserViewAPITestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
    def test_list_none(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])
    def test_list_user(self):
        user = User.objects.create(username='user')
        url = reverse('user-list')
        request = self.factory.get(url)
        response = resolve(url).func(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['url'],
                         reverse('user-detail', request=request, args=[user.username]))
        self.assertEqual(response.data['results'][0]['username'],
                         user.username)
    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'user',
            'email': 'user@example.com',
            'password': 'kW305U},jp2^',
        }
        request = self.factory.post(url, data)
        response = resolve(url).func(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'],
                         reverse('user-detail', request=request, args=[data['username']]))
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['graffiti'], [])
        self.assertEqual(response.data['add_graffiti'],
                         reverse('user-add-graffiti', request=request, args=[data['username']]))
