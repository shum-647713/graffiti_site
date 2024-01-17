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

class UserSerializer(serializers.ModelSerializer):
    graffiti = serializers.PrimaryKeyRelatedField(many=True, queryset=Graffiti.objects.all())
    class Meta:
        model = User
        fields = ['username', 'graffiti']
