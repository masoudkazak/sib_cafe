import datetime
from rest_framework import permissions


class IsFoodForToday(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        today = datetime.date.today().weekday()
        print(obj.days == today)
        return bool(
            obj.days == today or
            obj.days == 7
        )