import string
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Graffiti, Photo


class HyperlinkedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class HyperlinkedGraffitiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Graffiti
        fields = ['url', 'name']


class HyperlinkedPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ['url', 'image']


class UserSerializer(serializers.ModelSerializer):
    graffiti = HyperlinkedGraffitiSerializer(many=True, read_only=True)
    add_graffiti = serializers.HyperlinkedIdentityField(view_name='user-add-graffiti',
                                                        lookup_field='username')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'graffiti', 'add_graffiti']
        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = User(username = validated_data['username'],
                    email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.ModelField(model_field=User()._meta.get_field('username'))
    email = serializers.ModelField(model_field=User()._meta.get_field('email'),
                                   write_only=True)
    password = serializers.ModelField(model_field=User()._meta.get_field('password'),
                                      write_only=True)
    old_password = serializers.ModelField(model_field=User()._meta.get_field('password'),
                                          write_only=True, required=True)
    
    def validate_username(self, value):
        allowed = set(string.ascii_letters + string.digits + '@.+-_')
        if not set(value) <= allowed:
            raise serializers.ValidationError('Invalid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')
        return value
    
    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError('Incorrect old_password')
        return value
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if validated_data['password']:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class GraffitiSerializer(serializers.ModelSerializer):
    add_photo = serializers.HyperlinkedIdentityField(view_name='graffiti-add-photo')
    photos = HyperlinkedPhotoSerializer(many=True, read_only=True)
    owner = HyperlinkedUserSerializer(read_only=True)
    
    class Meta:
        model = Graffiti
        fields = ['name', 'owner', 'photos', 'add_photo']


class PhotoSerializer(serializers.ModelSerializer):
    graffiti = HyperlinkedGraffitiSerializer(read_only=True)
    
    class Meta:
        model = Photo
        fields = ['image', 'graffiti']
