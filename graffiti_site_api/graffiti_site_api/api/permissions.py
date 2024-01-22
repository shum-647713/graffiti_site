from rest_framework import permissions
from django.contrib.auth.models import User


class IsUserThemself(permissions.BasePermission):
    def has_permission(self, request, view):
        accessed_user = User.objects.get(username = view.kwargs['username'])
        return request.user == accessed_user
