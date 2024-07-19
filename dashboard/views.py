from django.utils import timezone
from django.db.models import Q
from django.views.generic import ListView, TemplateView
from loans.models import BookLoan


class OverduedLoanView(ListView):
    model = BookLoan
    template_name = "loans.html"
    paginate_by = 10

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
    paginate_by = 10

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
