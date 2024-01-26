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
        extra_kwargs = {
            'url': {'read_only': True},
        }

class UserSerializer(serializers.ModelSerializer):
    graffiti = HyperlinkedGraffitiSerializer(many=True)
    change_username = serializers.HyperlinkedIdentityField(view_name='user-username', lookup_field='username', read_only=True)
    change_password = serializers.HyperlinkedIdentityField(view_name='user-password', lookup_field='username', read_only=True)
    add_graffiti = serializers.HyperlinkedIdentityField(view_name='user-graffiti', lookup_field='username', read_only=True)
    class Meta:
        model = User
        fields = ['username', 'graffiti', 'change_username', 'change_password', 'add_graffiti']

class GraffitiSerializer(serializers.ModelSerializer):
    add_photo = serializers.HyperlinkedIdentityField(view_name='graffiti-photos', read_only=True)
    photos = HyperlinkedPhotoSerializer(many=True)
    owner = HyperlinkedUserSerializer()
    class Meta:
        model = Graffiti
        fields = ['name', 'photos', 'owner', 'add_photo']

class PhotoSerializer(serializers.ModelSerializer):
    graffiti = HyperlinkedGraffitiSerializer()
    class Meta:
        model = Photo
        fields = ['image', 'graffiti']

class UserNewUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UserNewPasswordSerializer(serializers.Serializer):
    password = serializers.ModelField(model_field=User()._meta.get_field('password'), write_only=True)
    old_password = serializers.CharField(max_length=128, write_only=True)
    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError('Incorrect old_password')
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
