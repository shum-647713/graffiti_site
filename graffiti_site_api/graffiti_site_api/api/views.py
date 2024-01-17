from graffiti_site_api.api import serializers
from django.contrib.auth.models import User
from rest_framework import generics


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.HyperlinkedUserSerializer

class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = serializers.UserSerializer
