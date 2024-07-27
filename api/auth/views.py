import json
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail

from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, TokenError

from .serializers import (
    User,
    Librarian,
    LibrarianSerializer,
    LibrarianLoginHistory,
    LoginHistorySerializer,
    Member,
    MemberSerializer,
    TokenSerializer,
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


class LibrarianLoginHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffUser]
    queryset = LibrarianLoginHistory.objects.all().order_by("date")
    serializer_class = LoginHistorySerializer

    filter_backends = [SearchFilter]
    search_fields = ["librarian__name"]


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

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(views.APIView):

    def get(self, request, *args, **kwargs):
        header = request.headers.get("Authorization")
        token = header.replace("Bearer ", "")

        try:
            verified_token = AccessToken(token=token)
        except TokenError:
            return Response(
                {"message": "Token is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user_id = verified_token.payload.get("user_id")
        user = User.objects.get(pk=user_id)
        data = {
            "id": user.pk,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
        }

        return Response(data, status=status.HTTP_200_OK)


class LoginBaseView(TokenObtainPairView):
    serializer_class = TokenSerializer
    user = None

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_403_FORBIDDEN,
            )

        self.user = user
        request.session["refresh_token"] = response.data.get("refresh")
        return response


class LibrarianLoginView(LoginBaseView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            if not self.user.is_staff:
                return Response(
                    {"message": "Account does not have access"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                pass

        return response


class RegisterBaseView(views.APIView):
    serializer_class = None

    def post(self, request):
        data = request.data
        data["message"] = "Register as librarian success"
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LibrarianRegisterView(RegisterBaseView):
    serializer_class = LibrarianSerializer


class MemberRegisterView(RegisterBaseView):
    serializer_class = MemberSerializer


class MemberLoginView(LoginBaseView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            if self.user.is_staff:
                return Response(
                    {"message": "Account does not have access"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                pass

        return response


class LogoutView(views.APIView):

    def get(self, request):
        refresh = request.session.get("refresh_token")
        if refresh is None:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        del request.session["refresh_token"]

        return Response({"message": "Logout success"}, status=status.HTTP_200_OK)


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

        return Response(
            {"message": "Change password failed, old password is invalid."},
            status=status.HTTP_403_FORBIDDEN,
        )


class TokenResetPasswordView(views.APIView):

    def post(self, request):
        data = request.data.copy()
        email = data.get("email")
        user = User.objects.get(email=email)

        if user is None:
            return Response(
                {"message": "Invalid Email, Request token reset password failed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        token = default_token_generator.make_token(user)
        message = f"Here's your reset password token: {token}"
        send_mail(
            subject="Django Library App Reset password token, dev: Ilham Maulana",
            message=message,
            from_email="from@example.com",
            recipient_list=["to@example.com"],
            fail_silently=False,
        )

        data["message"] = (
            "Your token request was successful! We've sent an email with instructions on how to use it."
        )

        self.request.session["user_id_reset_pw"] = user.id

        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(views.APIView):

    def post(self, request):
        data = request.data

        token = data.get("token")
        password1 = data.get("password1")
        password2 = data.get("password2")
        user_id = self.request.session["user_id_reset_pw"]
        user = User.objects.get(pk=user_id)

        is_password_invalid = password1 != password2
        if is_password_invalid:
            return Response(
                {"message": "password and confirm password are not same"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_token_valid = default_token_generator.check_token(user, token)
        if not is_token_valid:
            return Response(
                {"message": "Invalid token reset password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user.set_password(password1)
        user.save()

        del user_id
        return Response(
            {"message": "Reset password success"},
            status=status.HTTP_200_OK,
        )
