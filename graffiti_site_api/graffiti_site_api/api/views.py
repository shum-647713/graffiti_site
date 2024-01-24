from graffiti_site_api.api import serializers
from django.contrib.auth.models import User
from .models import Graffiti, Photo
from .permissions import IsUserThemself, IsGraffitiOwner
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


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

class PhotoRetrieve(generics.RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoSerializer

class GraffitiAddPhoto(generics.CreateAPIView):
    permission_classes = [IsGraffitiOwner]
    serializer_class = serializers.HyperlinkedPhotoSerializer
    def perform_create(self, serializer):
        graffiti = Graffiti.objects.get(pk = self.kwargs['pk'])
        serializer.save(graffiti = graffiti)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'auth': reverse('auth', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'graffiti': reverse('graffiti-list', request=request, format=format),
    })

@api_view(['GET'])
def api_auth(request, format=None):
    return Response({
        'login': reverse('auth:login', request=request, format=format),
        'logout': reverse('auth:logout', request=request, format=format),
    })
