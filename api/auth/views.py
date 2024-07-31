import random

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.authtoken.models import Token

from users.models import ResetPasswordPin

from .serializers import (
    User,
    Librarian,
    LibrarianSerializer,
    LibrarianLoginHistory,
    LoginHistorySerializer,
    Member,
    MemberSerializer,
    User,
    UserSerializer,
    UpdateProfileSerializer,
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

    def get(self, request):
        header = request.headers.get("Authorization")
        if header is None:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token = header.split(" ")[1]
        verified_token = Token.objects.filter(key=token)
        if not verified_token.exists():
            return Response(
                {"message": "Token is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user_id = verified_token[0].user.id
        user = User.objects.get(pk=user_id)

        account_id = None
        if user.is_staff:
            account_id = user.librarian.id
        else:
            account_id = user.member.id

        data = {
            "id": user.pk,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "account_id": account_id,
        }

        return Response(data, status=status.HTTP_200_OK)


class LoginBaseView(views.APIView):

    def post(self, request):
        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )
        if user:
            login(request=request, user=user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=401)


class LibrarianLoginView(LoginBaseView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            if not request.user.is_staff:
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
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(id=serializer.data["id"])
        login(request=request, user=user)
        token, created = Token.objects.get_or_create(user=user)

        response = serializer.data.copy()
        response["token"] = token.key
        return Response(response, status=status.HTTP_200_OK)


class LibrarianRegisterView(RegisterBaseView):
    serializer_class = UserSerializer


class MemberRegisterView(RegisterBaseView):
    serializer_class = UserSerializer

    def post(self, request):
        response = super().post(request)
        user_id = response.data.get("id")
        user = User.objects.get(pk=user_id)
        Member.objects.create(user=user)

        return response


class MemberLoginView(LoginBaseView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            if request.user.is_staff:
                return Response(
                    {"message": "Account does not have access"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                pass

        return response


class LogoutView(views.APIView):

    def get(self, request):
        header = request.headers.get("Authorization")
        if header is None:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token = header.split(" ")[1]
        verified_token = Token.objects.filter(key=token)
        if not verified_token.exists():
            return Response(
                {"message": "Token is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        verified_token.delete()
        logout(request=request)

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

    def generate_random_pin(self):
        return random.randint(10000000, 99999999)

    def store_data_with_pin(self, user):
        pin = self.generate_random_pin()
        ResetPasswordPin.objects.get_or_create(pin=pin, user=user)
        return pin

    def post(self, request):
        data = request.data.copy()
        email = data.get("email")
        user = User.objects.get(email=email)

        if user is None:
            return Response(
                {"message": "Invalid Email, Request pin reset password failed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        pin = self.store_data_with_pin(user)
        message = f"Here's your reset password pin:       {pin}"
        send_mail(
            subject="Django Library App Reset password pin, dev: Ilham Maulana",
            message=message,
            from_email="from@example.com",
            recipient_list=["to@example.com"],
            fail_silently=False,
        )

        data["message"] = (
            "Your pin request was successful! We've sent an email with instructions on how to use it."
        )

        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(views.APIView):

    def post(self, request):
        data = request.data

        pin = data.get("pin")
        password1 = data.get("password1")
        password2 = data.get("password2")
        encoded = None

        is_password_invalid = password1 != password2
        if is_password_invalid:
            return Response(
                {"message": "password and confirm password are not same"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            encoded = ResetPasswordPin.objects.get(pin=pin)
        except ResetPasswordPin.DoesNotExist:
            return Response(
                {"message": "Invalid pin reset password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        encoded.user.set_password(password1)
        encoded.user.save()
        encoded.delete()

        return Response(
            {"message": "Reset password success"},
            status=status.HTTP_200_OK,
        )


class UpdateProfileView(viewsets.ModelViewSet):
    serializer_class = UpdateProfileSerializer
    queryset = User.objects.all().order_by("id")

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_id = serializer.data.get("id")
        user = User.objects.get(pk=user_id)

        account_id = None
        if user.is_staff:
            account_id = user.librarian.id
        else:
            account_id = user.member.id

        response = serializer.data
        response["account_id"] = account_id
        return Response(response, status=status.HTTP_200_OK)
