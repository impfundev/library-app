import jwt
from django.conf import settings

from datetime import datetime, timedelta
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from authentications.utils import Hasher
from api.serializers import (
    get_user_model,
    UserSerializer,
    Book,
    BookSerializer,
    Members,
    MemberSerializer,
    Librarians,
    LibrarianSerializer,
    BookLoans,
    BookLoanSerializer,
)
from librarians.models import LoginHistory


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all().order_by("id")
    serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("created_at")
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["published_year", "category__name"]
    search_fields = filterset_fields


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Members.objects.all().order_by("created_at")
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name", "email"]
    search_fields = filterset_fields


class LibrarianViewSet(viewsets.ModelViewSet):
    queryset = Librarians.objects.all().order_by("created_at")
    serializer_class = LibrarianSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name", "email"]
    search_fields = filterset_fields


class BookLoanViewSet(viewsets.ModelViewSet):
    queryset = BookLoans.objects.all().order_by("created_at")
    serializer_class = BookLoanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        "loan_date",
        "due_date",
        "return_date",
    ]
    search_fields = filterset_fields


class LoginAsLibrarian(views.APIView):

    def post(self, request):
        data = request.data
        librarians = Librarians.objects.all()
        librarian = librarians.filter(email=data.get("email"))
        is_email_exists = librarian.exists()

        if not is_email_exists:
            return Response(
                {
                    "message": "Invalid Email, please enter valid email or sign up firts!"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        is_password_verified = Hasher.verify(
            data.get("password"), librarian[0].password
        )
        if not is_password_verified:
            return Response(
                {"message": "Invalid Password, please enter valid password!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        expiration_time = datetime.now() + timedelta(hours=2)
        payload = {
            "exp": expiration_time.timestamp(),
            "librarian_id": librarian[0].id,
            "name": librarian[0].name,
            "email": librarian[0].email,
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
        LoginHistory.objects.create(librarian_id=librarian[0].id)

        key = "auth_session_" + str(librarian[0].uuid)
        request.session[key] = token

        return Response({"message": "Login success!"}, status=status.HTTP_200_OK)


class LogoutAsLibrarian(views.APIView):

    def get(self, request, pk):
        librarian = Librarians.objects.get(pk=pk)
        key = "auth_session_" + str(librarian.uuid)
        if request.session[key] is None:
            return Response(
                {"message": "Logout failed, invalid key!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        del request.session[key]

        return Response({"message": "Logout success!"}, status=status.HTTP_200_OK)


class ChangePasswordAsLibrarian(views.APIView):

    def post(self, request, pk):
        data = request.data
        librarians = Librarians.objects.all()
        librarian = librarians.filter(pk=pk, email=data.get("email"))
        is_email_exists = librarian.exists()
        new_password = data.get("new_password")

        if not is_email_exists:
            return Response(
                {"message": "Invalid Email, please enter valid email!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_old_password_verified = Hasher.verify(
            data.get("password"), librarian[0].password
        )

        if not is_old_password_verified:
            return Response(
                {"message": "Invalid Old Password, please enter valid password!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if new_password is None:
            return Response(
                {"message": "Request failed, new_password is required field!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        hashed_password = Hasher.encode(new_password)
        librarian.update(password=hashed_password)

        return Response(
            {"message": "Change password success!"}, status=status.HTTP_200_OK
        )


class LoginAsMember(views.APIView):

    def post(self, request):
        data = request.data
        members = Members.objects.all()
        member = members.filter(email=data.get("email"))
        is_email_exists = member.exists()

        if not is_email_exists:
            return Response(
                {
                    "message": "Invalid Email, please enter valid email or sign up firts!"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        is_password_verified = Hasher.verify(data.get("password"), member[0].password)
        if not is_password_verified:
            return Response(
                {"message": "Invalid Password, please enter valid password!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        expiration_time = datetime.now() + timedelta(hours=2)
        payload = {
            "exp": expiration_time.timestamp(),
            "librarian_id": member[0].id,
            "name": member[0].name,
            "email": member[0].email,
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
        LoginHistory.objects.create(librarian_id=member[0].id)

        key = "auth_session_" + member[0].account_number
        request.session[key] = token

        return Response({"message": "Login success!"}, status=status.HTTP_200_OK)


class LogoutAsMember(views.APIView):

    def get(self, request, pk):
        member = Members.objects.get(pk=pk)
        key = "auth_session_" + member.account_number
        if request.session[key] is None:
            return Response(
                {"message": "Logout failed, invalid key!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        del request.session[key]

        return Response({"message": "Logout success!"}, status=status.HTTP_200_OK)


class ChangePasswordAsMember(views.APIView):

    def post(self, request, pk):
        data = request.data
        members = Members.objects.all()
        member = members.filter(pk=pk, email=data.get("email"))
        is_email_exists = member.exists()
        new_password = data.get("new_password")

        if not is_email_exists:
            return Response(
                {"message": "Invalid Email, please enter valid email!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_old_password_verified = Hasher.verify(
            data.get("password"), member[0].password
        )

        if not is_old_password_verified:
            return Response(
                {"message": "Invalid Old Password, please enter valid password!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if new_password is None:
            return Response(
                {"message": "Request failed, new_password is required field!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        hashed_password = Hasher.encode(new_password)
        member.update(password=hashed_password)

        return Response(
            {"message": "Change password success!"}, status=status.HTTP_200_OK
        )
