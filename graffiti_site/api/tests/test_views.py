from secrets import token_urlsafe
from pathlib import Path
from rest_framework.reverse import reverse
from rest_framework import test
from django.urls import resolve
from django.contrib.auth.models import User
from ..models import ActivationToken, Graffiti, Photo


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
    
    def update_user(self, data, partial):
        user = User.objects.create(username='user', email='user@example.com')
        user_password = 'kW305U},jp2^'
        user.set_password(user_password)
        user.save()
        
        url = reverse('user-detail', args=[user.username])
        data['old_password'] = user_password
        request = (self.factory.patch if partial else self.factory.put)(url, data)
        test.force_authenticate(request, user)
        response = resolve(url).func(request, username=user.username)
        return request, response
    
    def test_update_user(self):
        data = {
            'username': 'user_name',
            'email': 'user_name@example.com',
            'password': 'gK0RU14`S|Ix',
        }
        request, response = self.update_user(data=data, partial=False)
        
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
        __, response = self.update_user(data=data, partial=False)
        
        self.assertContains(response, text='Invalid username', status_code=400)
    
    def test_partially_update_user_invalid_username(self):
        data = {
            'username': 'user/name',
        }
        __, response = self.update_user(data=data, partial=True)
        
        self.assertContains(response, text='Invalid username', status_code=400)
    
    def test_activate_user(self):
        user = User.objects.create(username='user', is_active=False)
        token_value = token_urlsafe(32)
        token = ActivationToken.objects.create(value=token_value, user=user)
        
        url = reverse('user-activate')
        request = self.factory.get(url, {'token': token_value})
        request.method = 'post'
        response = resolve(url).func(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Location'],
                         reverse('user-detail', request=request, args=[user.username]))
        del user.is_active
        self.assertEqual(user.is_active, True)
        self.assertEqual(ActivationToken.objects.filter(pk=token.pk).count(), 0)
    
    def test_user_add_graffiti(self):
        user = User.objects.create(username='user')
        
        url = reverse('user-add-graffiti', args=[user.username])
        data = {'name': 'user\'s graffiti'}
        request = self.factory.post(url, data)
        test.force_authenticate(request, user)
        response = resolve(url).func(request, username=user.username)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Graffiti.objects.filter(owner=user).count(), 1)
        graffiti = Graffiti.objects.get(owner=user)
        self.assertEqual(response['Location'],
                         reverse('graffiti-detail', request=request, args=[graffiti.pk]))
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['owner']['url'],
                         reverse('user-detail', request=request, args=[user.username]))
        self.assertEqual(response.data['owner']['username'], user.username)
        self.assertEqual(response.data['photos'], [])
        self.assertEqual(response.data['add_photo'],
                         reverse('graffiti-add-photo', request=request, args=[graffiti.pk]))


class GraffitiViewAPITestCase(test.APITestCase):
    def setUp(self):
        self.factory = test.APIRequestFactory()
    
    def test_list_graffiti(self):
        user = User.objects.create(username='user')
        graffiti = Graffiti.objects.create(name='user\'s graffiti',
                                           owner=user)
        
        url = reverse('graffiti-list')
        request = self.factory.get(url)
        response = resolve(url).func(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['url'],
                         reverse('graffiti-detail', request=request, args=[graffiti.pk]))
        self.assertEqual(response.data['results'][0]['name'], graffiti.name)
    
    def test_create_graffiti(self):
        user = User.objects.create(username='user')
        
        url = reverse('graffiti-list')
        data = {'name': 'user\'s graffiti'}
        request = self.factory.post(url, data)
        test.force_authenticate(request, user)
        response = resolve(url).func(request)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Graffiti.objects.filter(owner=user).count(), 1)
        graffiti = Graffiti.objects.get(owner=user)
        self.assertEqual(response['Location'],
                         reverse('graffiti-detail', request=request, args=[graffiti.pk]))
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['owner']['url'],
                         reverse('user-detail', request=request, args=[user.username]))
        self.assertEqual(response.data['owner']['username'], user.username)
        self.assertEqual(response.data['photos'], [])
        self.assertEqual(response.data['add_photo'],
                         reverse('graffiti-add-photo', request=request, args=[graffiti.pk]))
    
    def test_retrieve_graffiti(self):
        user = User.objects.create(username='user')
        graffiti = Graffiti.objects.create(name='user\'s graffiti',
                                           owner=user)
        
        url = reverse('graffiti-detail', args=[graffiti.pk])
        request = self.factory.get(url)
        response = resolve(url).func(request, pk=graffiti.pk)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], graffiti.name)
        self.assertEqual(response.data['owner']['url'],
                         reverse('user-detail', request=request, args=[user.username]))
        self.assertEqual(response.data['owner']['username'], user.username)
        self.assertEqual(response.data['photos'], [])
        self.assertEqual(response.data['add_photo'],
                         reverse('graffiti-add-photo', request=request, args=[graffiti.pk]))
    
    def update_graffiti(self, partial):
        user = User.objects.create(username='user')
        graffiti = Graffiti.objects.create(name='user\'s graffiti',
                                           owner=user)
        
        url = reverse('graffiti-detail', args=[graffiti.pk])
        data = {'name': 'new name for user\'s graffiti'}
        request = (self.factory.patch if partial else self.factory.put)(url, data)
        test.force_authenticate(request, user)
        response = resolve(url).func(request, pk=graffiti.pk)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['owner']['url'],
                         reverse('user-detail', request=request, args=[user.username]))
        self.assertEqual(response.data['owner']['username'], user.username)
        self.assertEqual(response.data['photos'], [])
        self.assertEqual(response.data['add_photo'],
                         reverse('graffiti-add-photo', request=request, args=[graffiti.pk]))
    
    def test_update_graffiti(self):
        self.update_graffiti(partial=False)
    
    def test_partially_update_graffiti(self):
        self.update_graffiti(partial=True)
    
    def test_graffiti_add_photo(self):
        user = User.objects.create(username='user')
        graffiti = Graffiti.objects.create(name='user\'s graffiti',
                                           owner=user)
        image_ext = '.jpg'
        image_path = Path(__file__).resolve().parent / ('Graffiti-Style-Lettering' + image_ext)
        image_sha256hash = '0bfacc09f2fb9105c77988a230f30dc29897c5941a89c038b57c85407782b75f'
        testserver_images_url = 'http://testserver/media/images/'
        
        with open(image_path, "rb") as image_file:
            url = reverse('graffiti-add-photo', args=[graffiti.pk])
            data = {'image': image_file}
            request = self.factory.post(url, data)
            test.force_authenticate(request, user)
            response = resolve(url).func(request, pk=graffiti.pk)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Photo.objects.filter(graffiti=graffiti).count(), 1)
        photo = Photo.objects.get(graffiti=graffiti)
        self.assertEqual(response['Location'],
                         reverse('photo-detail', request=request, args=[photo.pk]))
        self.assertTrue(response.data['image'].startswith(testserver_images_url + image_sha256hash))
        self.assertTrue(response.data['image'].endswith(image_ext))
        self.assertEqual(response.data['graffiti']['url'],
                         reverse('graffiti-detail', request=request, args=[graffiti.pk]))
        self.assertEqual(response.data['graffiti']['name'], graffiti.name)
