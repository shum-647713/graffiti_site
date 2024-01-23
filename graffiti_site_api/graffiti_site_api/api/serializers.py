from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Graffiti, Photo


class HyperlinkedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password']
        extra_kwargs = {
            'url': {'lookup_field': 'username', 'read_only': True},
            'password': {'write_only': True},
        }
    def create(self, validated_data):
        user = User(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class HyperlinkedGraffitiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Graffiti
        fields = ['url', 'name']
        extra_kwargs = {
            'url': {'read_only': True},
        }

class HyperlinkedPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ['url', 'image']

class UserSerializer(serializers.ModelSerializer):
    graffiti = HyperlinkedGraffitiSerializer(many=True)
    add_graffiti = serializers.HyperlinkedIdentityField(view_name='user-graffiti', lookup_field='username', read_only=True)
    class Meta:
        model = User
        fields = ['username', 'graffiti', 'add_graffiti']

class GraffitiSerializer(serializers.ModelSerializer):
    photos = HyperlinkedPhotoSerializer(many=True)
    owner = HyperlinkedUserSerializer()
    class Meta:
        model = Graffiti
        fields = ['name', 'photos', 'owner']

class PhotoSerializer(serializers.ModelSerializer):
    graffiti = HyperlinkedGraffitiSerializer()
    class Meta:
        model = Photo
        fields = ['image', 'graffiti']
