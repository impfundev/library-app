import jwt
import json
import random
from django.utils import timezone

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate

from users.models import User, Member, ResetPasswordPin
from loans.models import Book, BookLoan


@csrf_exempt
def loginUserView(request):

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse(
                {"message": "Username or Password is incorrect"}, status=400
            )

        expired = timezone.now() + timezone.timedelta(days=1)
        payload = {"user_id": user.pk, "exp": expired}
        token = jwt.encode(payload, key="secret", algorithm="HS256")
        return JsonResponse(
            {"message": "Login successful", "token": token},
            status=201,
        )


@csrf_exempt
def registerUserView(request):
    users = User.objects.all()

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        is_username = users.filter(username=username)
        is_email = users.filter(email=email)

        if is_username.exists() or is_email.exists():
            return JsonResponse(
                {"message": "Username or email already exists"}, status=400
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        expired = timezone.now() + timezone.timedelta(days=1)
        payload = {"user_id": user.pk, "exp": expired}
        token = jwt.encode(payload, key="secret", algorithm="HS256")
        data = {
            "message": "register successful",
            "token": token,
        }
        return JsonResponse(data, status=201, safe=False)


@csrf_exempt
def logoutUserView(request):

    if request.method == "GET":
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def getUserDetail(request):
    if request.method == "GET":
        header_authorization = request.headers.get("Authorization")
        try:
            token = header_authorization.split(" ")[1]
            payload = jwt.decode(token, key="secret", algorithms=["HS256"])
            user = User.objects.get(pk=payload["user_id"])
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
            }
            return JsonResponse(data, status=200, safe=False)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message": "Unauthorized"}, status=401)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def updateUserProfileView(request):
    users = User.objects.all()

    if request.method == "PUT":
        data = json.loads(request.body)
        header_authorization = request.headers.get("Authorization")
        try:
            token = header_authorization.split(" ")[1]
            payload = jwt.decode(token, key="secret", algorithms=["HS256"])
            user = User.objects.get(pk=payload["user_id"])

            if data.get("username") != user.username:
                is_username = users.filter(username=data.get("username"))
                if is_username.exists():
                    return JsonResponse(
                        {"message": "Username already exists"}, status=400
                    )

            if data.get("email") != user.email:
                is_email = users.filter(email=data.get("email"))
                if is_email.exists():
                    return JsonResponse({"message": "Email already exists"}, status=400)

            user.username = data.get("username", user.username)
            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.email = data.get("email", user.email)
            user.save()

            return JsonResponse(
                {"message": "User profile updated successfully"}, status=200
            )

        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message": "Unauthorized"}, status=401)

    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def changePasswordView(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        header_authorization = request.headers.get("Authorization")

        try:
            token = header_authorization.split(" ")[1]
            payload = jwt.decode(token, key="secret", algorithms=["HS256"])
            user = User.objects.get(pk=payload["user_id"])
            old_password = data.get("old_password")
            new_password1 = data.get("new_password1")
            new_password2 = data.get("new_password2")

            if not user.check_password(old_password):
                return JsonResponse(
                    {"message": "Invalid old password"},
                    status=400,
                )

            if new_password1 != new_password2:
                return JsonResponse(
                    {"message": "Passwords and confirm password do not match"},
                    status=400,
                )

            user.set_password(str(new_password1))
            user.save()

            return JsonResponse({"message": "Change password successful"}, status=200)

        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message": "Unauthorized"}, status=401)

    return JsonResponse({"message": "Invalid request method"}, status=405)


def generate_random_pin():
    return random.randint(10000000, 99999999)


def store_data_with_pin(user):
    is_pin = ResetPasswordPin.objects.filter(user=user).first()
    if is_pin is None:
        pin = generate_random_pin()
        ResetPasswordPin.objects.create(pin=generate_random_pin(), user=user)
    else:
        pin = is_pin.pin
    return pin


@csrf_exempt
def resetPasswordView(request):
    users = User.objects.all()

    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        try:
            user = users.get(email=email)
            pin = store_data_with_pin(user)

            message = f"Here's your reset password pin:       {pin}"
            user.email_user(
                subject="Django Library App Reset password pin, dev: Ilham Maulana",
                message=message,
                from_email="from@example.com",
                fail_silently=False,
            )
            return JsonResponse(
                {"message": "Pin reset password sent successfully to your email"},
                status=200,
            )
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "User with this email does not exist"}, status=400
            )

    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def resetPasswordConfirmView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        password1 = data.get("password1")
        password2 = data.get("password2")
        pin = data.get("pin")

        if password1 is None or password2 is None:
            return JsonResponse(
                {"message": "Password and confirm password are required"}, status=400
            )

        if password1 != password2:
            return JsonResponse(
                {"message": "Password and confirm password do not match"}, status=400
            )

        if pin is None:
            return JsonResponse({"message": "Pin is required"}, status=400)

        pin = ResetPasswordPin.objects.filter(pin=pin).first()
        if pin is None:
            return JsonResponse({"message": "Pin is invalid"}, status=400)

        if password1 != password2:
            return JsonResponse(
                {"message": "Passwords and confirm password do not match"},
                status=400,
            )

        pin.user.set_password(password1)
        pin.delete()
        return JsonResponse({"message": "Password reset successful"}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def checkAuthSessionView(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return JsonResponse(
                {"message": "User is authenticated", "authenticated": True}, status=200
            )
        else:
            return JsonResponse(
                {"message": "User is not authenticated", "authenticated": False},
                status=401,
            )
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def memberLoanView(request):
    header_authorization = request.headers.get("Authorization")
    book_loans = BookLoan.objects.all().order_by("loan_date")

    if request.method == "GET":
        now = timezone.now()
        due_date_treshold = now + timezone.timedelta(days=3)
        near_outstanding = request.GET.get("near_outstanding")
        overdue = request.GET.get("overdue")
        page_number = request.GET.get("page", 1)

        try:
            token = header_authorization.split(" ")[1]
            payload = jwt.decode(token, key="secret", algorithms=["HS256"])
            user = User.objects.get(pk=payload["user_id"])
            member = Member.objects.filter(user=user).first()

            if member is None:
                return JsonResponse({"message": "Member not found"}, status=404)

            is_loans = book_loans.filter(member=member).first()
            if is_loans is None:
                return JsonResponse({"message": "No loans found"}, status=404)

            loans = book_loans.filter(member=member)
            if near_outstanding:
                loans = (
                    loans.filter(due_date__lte=due_date_treshold, return_date=None)
                    .filter(due_date__gte=now)
                    .order_by("loan_date")
                )

            if overdue:
                loans = loans.filter(due_date__lte=now, return_date=None)

            paginator = Paginator(loans, 10)
            page_obj = paginator.get_page(page_number)

            data = []
            for loan in page_obj:
                remaining_loan_time = str(loan.due_date.day - now.day) + " days left"
                is_overdue = loan.due_date < now
                loan_obj = {
                    "book": {
                        "id": loan.book.id,
                        "title": loan.book.title,
                        "author": loan.book.author,
                        "description": loan.book.description,
                        "cover_image": loan.book.cover_image.url,
                    },
                    "remaining_loan_time": remaining_loan_time,
                    "is_overdue": is_overdue,
                    "loan_date": loan.loan_date,
                    "due_date": loan.due_date,
                }
                data.append(loan_obj)

            response_data = {
                "data": data,
                "has_next": page_obj.has_next(),
                "has_prev": page_obj.has_previous(),
                "page_number": page_obj.number,
                "total_pages": paginator.num_pages,
            }

            return JsonResponse(response_data, safe=False, status=200)

        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message": "Unauthorized"}, status=401)

    if request.method == "POST":
        data = json.loads(request.body)
        book_id = data.get("book")
        member_id = data.get("member")
        loan_date = data.get("loan_date")
        due_date = data.get("due_date")

        try:
            token = header_authorization.split(" ")[1]
            jwt.decode(token, key="secret", algorithms=["HS256"])
            member = Member.objects.filter(user__pk=member_id).first()
            book = Book.objects.filter(pk=book_id).first()

            if member is None:
                return JsonResponse({"message": "Member not found"}, status=404)

            if book is None:
                return JsonResponse({"message": "Book not found"}, status=404)

            book_loans.create(
                member=member, book=book, loan_date=loan_date, due_date=due_date
            )
            return JsonResponse(
                {"message": "create loan successfull"}, safe=False, status=200
            )

        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message": "Unauthorized"}, status=401)

    return JsonResponse({"message": "Invalid request method"}, status=405)
