import jwt
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from loans.models import BookLoan


@csrf_exempt
def bookLoanView(request):
    header_authorization = request.headers.get("Authorization")

    if request.method == "GET":
        now = timezone.now()
        due_date_treshold = now + timezone.timedelta(days=3)
        loans = BookLoan.objects.all().order_by("loan_date")
        near_outstanding = request.GET.get("near_outstanding")
        overdue = request.GET.get("overdue")

        try:
            token = header_authorization.split(" ")[1]
            jwt.decode(token, key="secret", algorithms=["HS256"])
            if near_outstanding:
                loans = (
                    loans.filter(due_date__lte=due_date_treshold, return_date=None)
                    .filter(due_date__gte=now)
                    .order_by("loan_date")
                )

            if overdue:
                loans = loans.filter(due_date__lte=now, return_date=None).order_by(
                    "loan_date"
                )

            data = []
            for loan_item in loans:
                remaining_loan_time = (
                    str(loan_item.due_date.day - now.day) + " days left"
                )
                is_overdue = loan_item.due_date < now
                loan_obj = {
                    "book": {
                        "id": loan_item.book.id,
                        "title": loan_item.book.title,
                        "author": loan_item.book.author,
                        "description": loan_item.book.description,
                        "cover_image": loan_item.book.cover_image.url,
                    },
                    "user": {
                        "id": loan_item.member.user.id,
                        "username": loan_item.member.user.username,
                        "email": loan_item.member.user.email,
                        "first_name": loan_item.member.user.first_name,
                        "last_name": loan_item.member.user.last_name,
                        "is_staff": loan_item.member.user.is_staff,
                    },
                    "remaining_loan_time": remaining_loan_time,
                    "is_overdue": is_overdue,
                    "loan_date": loan_item.loan_date,
                    "due_date": loan_item.due_date,
                }
                data.append(loan_obj)

            return JsonResponse(data, safe=False, status=200)

        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message": "Unauthorized"}, status=401)

    return JsonResponse({"message": "Invalid request method"}, status=405)
