from rest_framework.reverse import reverse
from rest_framework import test
from django.urls import resolve
from django.contrib.auth.models import User


class UserViewAPITestCase(test.APITestCase):
    def setUp(self):
        self.factory = test.APIRequestFactory()
    
    def test_list_no_users(self):
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
    
    def test_retrieve_user(self):
        user = User.objects.create(username='user')
        
        url = reverse('user-detail', args=[user.username])
        request = self.factory.get(url)
        response = resolve(url).func(request, username=user.username)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['graffiti'], [])
        self.assertEqual(response.data['add_graffiti'],
                         reverse('user-add-graffiti', request=request, args=[user.username]))
    
    def update_user(self, method, data):
        assert method in ['put', 'patch']
        
        user = User.objects.create(username='user', email='user@example.com')
        user_password = 'kW305U},jp2^'
        user.set_password(user_password)
        user.save()
        
        url = reverse('user-detail', args=[user.username])
        data['old_password'] = user_password
        if method == 'put':
            request = self.factory.put(url, data)
        else:
            request = self.factory.patch(url, data)
        test.force_authenticate(request, user)
        response = resolve(url).func(request, username=user.username)
        return request, response
    
    def test_update_user(self):
        data = {
            'username': 'user_name',
            'email': 'user_name@example.com',
            'password': 'gK0RU14`S|Ix',
        }
        request, response = self.update_user(method='put', data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Location'],
                         reverse('user-detail', request=request, args=[data['username']]))
        self.assertEqual(response.data['username'], data['username'])
    
    def test_update_user_invalid_username(self):
        data = {
            'username': 'name_user\\',
            'email': 'name_user@u.com',
            'password': '4G0>6db&qI[t',
        }
        __, response = self.update_user(method='put', data=data)
        
        self.assertContains(response, text='Invalid username', status_code=400)
    
    def test_partially_update_user_invalid_username(self):
        data = {
            'username': 'user/name',
        }
        __, response = self.update_user(method='patch', data=data)
        
        self.assertContains(response, text='Invalid username', status_code=400)
