from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method != "POST" and not request.user.is_staff:
            return False
        elif request.method != "POST" and not request.user.is_authenticated:
            return False

        return True


class IsNotStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method != "POST" and request.user.is_staff:
            return False
        elif request.method != "POST" and not request.user.is_authenticated:
            return False

        return True
