from . import serializers
from django.contrib.auth.models import User
from .models import Graffiti, Photo
from .permissions import IsUserThemself, IsGraffitiOwner
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-pk')
    lookup_field = 'username'
    def get_serializer_class(self):
        match self.action:
            case 'list':
                return serializers.HyperlinkedUserSerializer
            case 'create' | 'retrieve':
                return serializers.UserSerializer
            case 'update' | 'partial_update':
                return serializers.UserUpdateSerializer
            case 'add_graffiti':
                return serializers.GraffitiSerializer
    def get_permissions(self):
        match self.action:
            case 'list' | 'create' | 'retrieve' | None:
                permission_classes = []
            case 'update' | 'partial_update' | 'destroy' | 'add_graffiti':
                permission_classes = [IsUserThemself]
        return [permission() for permission in permission_classes]
    def update(self, request, *args, **kwargs):
        username = super().update(request, *args, **kwargs).data['username']
        response = HttpResponse(content="", status=303)
        response["Location"] = reverse('user-detail', request=request, args=[username])
        return response
    @action(detail=True, methods=['post'])
    def add_graffiti(self, request, username=None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner = user)
        return Response()

class GraffitiViewSet(viewsets.ModelViewSet):
    queryset = Graffiti.objects.all().order_by('-pk')
    def get_serializer_class(self):
        match self.action:
            case 'list':
                return serializers.HyperlinkedGraffitiSerializer
            case 'create' | 'retrieve' | 'update' | 'partial_update':
                return serializers.GraffitiSerializer
            case 'add_photo':
                return serializers.PhotoSerializer
    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve' | None:
                permission_classes = []
            case 'create':
                permission_classes = [IsAuthenticated]
            case 'update' | 'partial_update' | 'destroy' | 'add_photo':
                permission_classes = [IsGraffitiOwner]
        return [permission() for permission in permission_classes]
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
    @action(detail=True, methods=['post'])
    def add_photo(self, request, pk=None):
        graffiti = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(graffiti = graffiti)
        return Response()

class PhotoList(generics.ListAPIView):
    queryset = Photo.objects.all().order_by('-pk')
    serializer_class = serializers.HyperlinkedPhotoSerializer

class PhotoDetail(generics.RetrieveDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'auth': reverse('auth-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'graffiti': reverse('graffiti-list', request=request, format=format),
        'photos': reverse('photo-list', request=request, format=format),
    })

@api_view(['GET'])
def auth_list(request, format=None):
    return Response({
        'login': reverse('auth:login', request=request, format=format),
        'logout': reverse('auth:logout', request=request, format=format),
    })
