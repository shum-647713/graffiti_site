from graffiti_site_api.api import serializers
from django.contrib.auth.models import User
from .models import Graffiti
from .permissions import IsUserThemself
from rest_framework import generics, permissions


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.HyperlinkedUserSerializer

class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = serializers.UserSerializer

class GraffitiListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Graffiti.objects.all()
    serializer_class = serializers.HyperlinkedGraffitiSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GraffitiRetrieve(generics.RetrieveAPIView):
    queryset = Graffiti.objects.all()
    serializer_class = serializers.GraffitiSerializer

class UserAddGraffiti(generics.CreateAPIView):
    permission_classes = [IsUserThemself]
    serializer_class = serializers.HyperlinkedGraffitiSerializer
    def perform_create(self, serializer):
        owner = User.objects.get(username = self.kwargs['username'])
        serializer.save(owner = owner)
