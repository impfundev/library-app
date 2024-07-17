from django.contrib.auth import authenticate, login, logout
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from .serializers import (
    Librarian,
    LibrarianSerializer,
    LibrarianLoginHistory,
    LoginHistorySerializer,
    Member,
    MemberSerializer,
)
from .permissions import IsStaffUser, IsNotStaffUser


class LibrarianViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffUser]
    queryset = Librarian.objects.all().order_by("created_at")
    serializer_class = LibrarianSerializer

    filter_backends = [SearchFilter]
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = [IsNotStaffUser]
    queryset = Member.objects.all().order_by("created_at")
    serializer_class = MemberSerializer

    filter_backends = [SearchFilter]
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]

    def list(self, request):
        if self.request.user.is_staff:
            return Response(
                {"message": "Access Denied"}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

                librarian = Librarian.objects.get(user=self.user)
                LibrarianLoginHistory.objects.create(librarian=librarian)

        return response


class LibrarianLoginHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffUser]
    queryset = LibrarianLoginHistory.objects.all().order_by("date")
    serializer_class = LoginHistorySerializer

    filter_backends = [SearchFilter]
    search_fields = ["librarian__name"]


class LibrarianViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffUser]
    queryset = Librarian.objects.all().order_by("created_at")
    serializer_class = LibrarianSerializer

    filter_backends = [SearchFilter]
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class MemberChangePasswordView(views.APIView):
    permission_classes = [IsNotStaffUser]

    def post(self, request, member_id):
        new_password = request.data.get("new_password")
        old_password = request.data.get("old_password")
        member = Member.objects.get(pk=member_id)
        user = member.user

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Pasword succesfuly changed"}, status=status.HTTP_200_OK
            )

        return Response({"message": "Change password failed, old password is invalid."})
