from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class IsStaffUser(IsAuthenticated):

    def has_permission(self, request, view):
        refresh_token = request.session.get("refresh_token")

        return bool(
            refresh_token is not None
            and request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class IsNotStaffUser(IsAuthenticated):

    def has_permission(self, request, view):
        refresh_token = request.session.get("refresh_token")
        return bool(
            refresh_token is not None
            and request.user
            and request.user.is_authenticated
            and not request.user.is_staff
        )
