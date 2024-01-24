from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Graffiti


class IsUserThemself(permissions.BasePermission):
    def has_permission(self, request, view):
        accessed_user = User.objects.get(username = view.kwargs['username'])
        return request.user == accessed_user

class IsGraffitiOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        accessed_graffiti = Graffiti.objects.get(pk = view.kwargs['pk'])
        return request.user == accessed_graffiti.owner
