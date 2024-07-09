from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import render
from datetime import datetime, timedelta

from librarians.models import LoginHistory
from members.models import Members
from book_loans.models import Book, BookLoans


class OverduedLoanView(ListView):
    model = BookLoans
    template_name = "loans.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        now = datetime.now()
        queryset = queryset.filter(due_date__lte=now, return_date=None).order_by(
            "-updated_at"
        )

        if keyword:
            queryset = queryset.filter(
                Q(book__title__icontains=keyword)
                | Q(member__name__icontains=keyword)
                | Q(librarian__name__icontains=keyword)
            ).order_by("-created_at")

        if order:
            if order == "new":
                queryset = queryset.order_by("-created_at")
            elif order == "old":
                queryset = queryset.order_by("created_at")

        return queryset


class UpcomingLoanView(ListView):
    model = BookLoans
    template_name = "loans.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        now = datetime.now()
        due_date_treshold = now.today() + timedelta(days=3)

        queryset = (
            queryset.filter(due_date__lte=due_date_treshold, return_date=None)
            .filter(due_date__gte=now.today())
            .order_by("-updated_at")
        )

        if keyword:
            queryset = queryset.filter(
                Q(book__title__icontains=keyword)
                | Q(member__name__icontains=keyword)
                | Q(librarian__name__icontains=keyword)
            ).order_by("-created_at")

        if order:
            if order == "new":
                queryset = queryset.order_by("-created_at")
            elif order == "old":
                queryset = queryset.order_by("created_at")

        return queryset


def home(request):
    return render(request, "homepage.html")


def index(request):
    latest_login_history = LoginHistory.objects.order_by("-login_at")[:10]
    total_book = Book.objects.count()
    total_member = Members.objects.count()
    total_book_loans = BookLoans.objects.count()

    now = datetime.now()
    overdue_loans = BookLoans.objects.filter(
        due_date__lte=now, return_date=None
    ).order_by("created_at")

    due_date_treshold = now.today() + timedelta(days=3)

    upcoming_loans = BookLoans.objects.filter(
        due_date__lte=due_date_treshold, return_date=None
    ).filter(due_date__gte=now.today())

    context = {
        "login_histories": latest_login_history,
        "total_book": total_book,
        "total_member": total_member,
        "total_book_loans": total_book_loans,
        "total_overdue": overdue_loans.count(),
        "overdue_loans": overdue_loans,
        "upcoming_loans": upcoming_loans,
    }

    if overdue_loans.exists():
        context["overdue_loans"] = overdue_loans

    return render(request, "dashboard/index.html", context)
