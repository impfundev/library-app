from django.shortcuts import render
from librarians.models import LoginHistory
from members.models import Members
from book_loans.models import Book, BookLoans


def home(request):
    return render(request, "homepage.html")


def index(request):
    latest_login_history = LoginHistory.objects.order_by("login_at")[:10]
    total_book = Book.objects.count()
    total_member = Members.objects.count()
    total_book_loans = BookLoans.objects.count()
    context = {
        "login_histories": latest_login_history,
        "total_book": total_book,
        "total_member": total_member,
        "total_book_loans": total_book_loans,
    }

    return render(request, "dashboard/index.html", context)
