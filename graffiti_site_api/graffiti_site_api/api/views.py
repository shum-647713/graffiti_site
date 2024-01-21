from graffiti_site_api.api import serializers
from django.contrib.auth.models import User
from .models import Graffiti
from rest_framework import generics


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.HyperlinkedUserSerializer

class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = serializers.UserSerializer

class GraffitiList(generics.ListAPIView):
    queryset = Graffiti.objects.all()
    serializer_class = serializers.HyperlinkedGraffitiSerializer

class GraffitiRetrieve(generics.RetrieveAPIView):
    queryset = Graffiti.objects.all()
    serializer_class = serializers.GraffitiSerializer
