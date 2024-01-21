from rest_framework import serializers
from django.contrib.auth.models import User
from graffiti_site_api.api.models import Graffiti


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

class UserSerializer(serializers.ModelSerializer):
    graffiti = HyperlinkedGraffitiSerializer(many=True)
    class Meta:
        model = User
        fields = ['username', 'graffiti']

class GraffitiSerializer(serializers.ModelSerializer):
    owner = HyperlinkedUserSerializer()
    class Meta:
        model = Graffiti
        fields = ['name', 'owner']
