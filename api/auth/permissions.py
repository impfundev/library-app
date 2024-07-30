from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class IsStaffUser(IsAuthenticated):

    def has_permission(self, request, view):
        header = request.headers.get("Authorization")

        token = header.split(" ")[1]
        verified_token = None

        try:
            verified_token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return False

        return bool(
            header is not None
            and verified_token is not None
            and verified_token.user.is_staff
        )


class IsNotStaffUser(IsAuthenticated):

    def has_permission(self, request, view):
        header = request.headers.get("Authorization")

        token = header.split(" ")[1]
        verified_token = None

        try:
            verified_token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return False

        return bool(
            header is not None
            and verified_token is not None
            and not verified_token.user.is_staff
        )
