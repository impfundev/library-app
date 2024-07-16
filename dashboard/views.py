from django.utils import timezone
from django.db.models import Q
from django.views.generic import ListView, TemplateView

from users.models import LibrarianLoginHistory, Member
from book.models import Category, Book
from loans.models import BookLoan


class OverduedLoanView(ListView):
    model = BookLoan
    template_name = "loans.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        now = timezone.now()
        queryset = queryset.filter(due_date__lte=now, return_date=None).order_by(
            "-created_at"
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
    model = BookLoan
    template_name = "loans.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        now = timezone.now()
        due_date_treshold = now + timezone.timedelta(days=3)

        queryset = (
            queryset.filter(due_date__lte=due_date_treshold, return_date=None)
            .filter(due_date__gte=now)
            .order_by("-created_at")
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


class HomePage(TemplateView):
    template_name = "homepage.html"


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"

    login_history = LibrarianLoginHistory.objects.order_by("-date")[:10]
    book_loans = BookLoan.objects.all()
    total_book = Book.objects.count()
    total_category = Category.objects.count()
    total_member = Member.objects.count()
    total_book_loans = book_loans.count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        overdue_loans = self.book_loans.filter(
            due_date__lte=now, return_date=None
        ).order_by("-due_date")[:10]

        due_date_treshold = now + timezone.timedelta(days=3)

        upcoming_loans = (
            self.book_loans.filter(due_date__lte=due_date_treshold, return_date=None)
            .filter(due_date__gte=now)
            .order_by("-due_date")[:10]
        )

        context["login_histories"] = self.login_history
        context["total_book"] = self.total_book
        context["total_category"] = self.total_category
        context["total_member"] = self.total_member
        context["total_book_loans"] = self.total_book_loans
        context["total_overdue"] = overdue_loans.count()
        context["total_upcoming"] = upcoming_loans.count()
        context["overdue_loans"] = overdue_loans
        context["upcoming_loans"] = upcoming_loans

        return context
