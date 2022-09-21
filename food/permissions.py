import datetime
from rest_framework import permissions


class TimePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        if time >= '12:00:00':
            return False
        return True


class IsUserOrdered(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.username == request.user.username


class IsCanCancelOrder(permissions.BasePermission):
    def has_permission(self, request, view):
        start = '12:00:00'
        end = '14:00:00'
        now = datetime.datetime.now().strftime("%H:%M:%S")
        
        if now >= start and now <= end:
            return True
        return False
        return True
