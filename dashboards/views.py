from datetime import datetime, timedelta
from django.shortcuts import render
from librarians.models import LoginHistory
from members.models import Members
from book_loans.models import Book, BookLoans


def home(request):
    return render(request, "homepage.html")


def index(request):
    latest_login_history = LoginHistory.objects.order_by("-login_at")[:10]
    total_book = Book.objects.count()
    total_member = Members.objects.count()
    total_book_loans = BookLoans.objects.count()

    now = datetime.now()
    overdue_loans = BookLoans.objects.filter(due_date__lte=now)

    context = {
        "login_histories": latest_login_history,
        "total_book": total_book,
        "total_member": total_member,
        "total_book_loans": total_book_loans,
        "total_overdue": overdue_loans.count(),
    }

    if overdue_loans.exists():
        context["overdue_loans"] = overdue_loans
        for loan in BookLoans.objects.all():
            near_overdue_window = loan.due_date - timedelta(days=7)
            due_date = loan.due_date

        near_overdue_loans = BookLoans.objects.filter(
            due_date__range=(near_overdue_window, due_date)
        )
        context["near_overdue_loans"] = near_overdue_loans

    return render(request, "dashboard/index.html", context)
