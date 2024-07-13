from django.contrib.auth import authenticate, login, logout
from rest_framework import views, viewsets, permissions, status
from rest_framework.response import Response

from .serializers import (
    Librarian,
    LibrarianSerializer,
    Member,
    MemberSerializer,
)


class LibrarianViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Librarian.objects.all().order_by("created_at")
    serializer_class = LibrarianSerializer

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Member.objects.all().order_by("created_at")
    serializer_class = MemberSerializer

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginBaseView(views.APIView):
    user = None

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if request.user.is_authenticated:
            return Response(
                {"message": "Login failed, user is already authenticated"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if username is None or password is None:
            return Response(
                {"message": "Login failed, username or password cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            self.user = user
            request.data["token"] = user.get_session_auth_hash()
            request.data["message"] = "Login successful"

            return Response(request.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Login failed, invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LibrarianLoginView(LoginBaseView):
    def post(self, request):
        response = super().post(request)

        if response.status_code == status.HTTP_200_OK:
            if not self.user.is_staff:
                return Response(
                    {"message": "Login as librarian failed, account is not staff"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                login(request, self.user)

        return response


class MemberLoginView(LoginBaseView):
    def post(self, request):
        response = super().post(request)

        if response.status_code == status.HTTP_200_OK:
            if self.user.is_staff:
                return Response(
                    {"message": "Login failed, invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                login(request, self.user)

        return response


class LogoutBasedView(views.APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Logout failed, user is unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response({"message": "Logout success"}, status=status.HTTP_200_OK)


class LibrarianLogoutView(LogoutBasedView):

    def get(self, request):
        response = super().get(request)
        if response.status_code == status.HTTP_200_OK:
            if request.user.is_staff:
                logout(request)
            else:
                return Response(
                    {"message": "Logout failed, user is unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return response


class MemberLogoutView(LogoutBasedView):

    def get(self, request):
        response = super().get(request)
        if response.status_code == status.HTTP_200_OK:
            if not request.user.is_staff:
                logout(request)
            else:
                return Response(
                    {"message": "Logout failed, user is unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return response
