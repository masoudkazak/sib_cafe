import datetime
from rest_framework import permissions


class TimePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        if time >= '12:00:00':
            return False
        return True