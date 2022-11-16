import datetime
from rest_framework import permissions


class IsUserOrdered(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.username == request.user.username

