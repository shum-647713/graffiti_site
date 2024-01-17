from graffiti_site_api.api import serializers
from django.contrib.auth.models import User
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return serializers.HyperlinkedUserSerializer
        else:
            return serializers.UserSerializer
