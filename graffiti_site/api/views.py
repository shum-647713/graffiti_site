from secrets import token_urlsafe
from rest_framework.serializers import Serializer as EmptySerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.exceptions import ParseError
from rest_framework.decorators import api_view, action
from rest_framework import generics, viewsets, status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from .permissions import IsUserThemself, IsGraffitiOwner, IsPhotoOwner
from .models import ActivationToken, Graffiti, Photo
from .email import send_activation_link
from . import serializers


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
            case 'activate':
                return EmptySerializer
            case 'add_graffiti':
                return serializers.GraffitiSerializer
    
    def get_permissions(self):
        match self.action:
            case 'list' | 'create' | 'retrieve' | 'activate' | None:
                permission_classes = []
            case 'update' | 'partial_update' | 'destroy' | 'add_graffiti':
                permission_classes = [IsUserThemself]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(is_active = not settings.ENABLE_EMAIL)
        
        if settings.ENABLE_EMAIL:
            token_value = token_urlsafe(32)
            ActivationToken.objects.create(value=token_value, user=instance)
            
            link = reverse('user-activate', request=request)
            link = f"{link}?token={token_value}"
            send_activation_link(link, instance.email)
        
        headers = {'Location': reverse('user-detail', request=request, args=[instance.username])}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['post'])
    def activate(self, request):
        token_value = request.query_params.get('token', None)
        if token_value is None:
            raise ParseError(detail='Query parameter "token" is missing.')
        token = get_object_or_404(ActivationToken, value=token_value)
        user = token.user
        user.is_active = True
        user.save()
        token.delete()
        headers = {'Location': reverse('user-detail', request=request, args=[user.username])}
        return Response(headers=headers)
    
    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs).data
        headers = {'Location': reverse('user-detail', request=request, args=[data['username']])}
        return Response(data, headers=headers)
    
    @action(detail=True, methods=['post'])
    def add_graffiti(self, request, username=None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner = user)
        headers = {'Location': reverse('graffiti-detail', request=request, args=[instance.pk])}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner = self.request.user)
        headers = {'Location': reverse('graffiti-detail', request=request, args=[instance.pk])}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def add_photo(self, request, pk=None):
        graffiti = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(graffiti = graffiti)
        headers = {'Location': reverse('photo-detail', request=request, args=[instance.pk])}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PhotoList(generics.ListAPIView):
    queryset = Photo.objects.all().order_by('-pk')
    serializer_class = serializers.HyperlinkedPhotoSerializer


class PhotoDetail(generics.RetrieveDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            permission_classes = []
        else:
            permission_classes = [IsPhotoOwner]
        return [permission() for permission in permission_classes]


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
