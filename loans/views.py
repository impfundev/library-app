from django.db.models import F
from django.utils import timezone
from django.db.models import Q
from django.views import generic
from .models import BookLoan
from .forms import BookLoanForm


class BookLoanListView(generic.ListView):
    model = BookLoan
    template_name = "loans.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        if keyword:
            queryset = queryset.filter(
                Q(book__title__icontains=keyword)
                | Q(member__user__username__icontains=keyword)
            ).order_by("-created_at")

        if order:
            if order == "new":
                queryset = queryset.order_by("-created_at")
            elif order == "old":
                queryset = queryset.order_by("created_at")

        today = timezone.now()
        queryset = queryset.annotate(remaining_loan_time=(F("due_date") - today))

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class BookLoanCreateView(generic.edit.CreateView):
    model = BookLoan
    form_class = BookLoanForm
    success_url = "/book-loans"
    template_name = "form/create_form.html"


class BookLoanUpdateView(generic.edit.UpdateView):
    model = BookLoan
    form_class = BookLoanForm
    success_url = "/book-loans"
    template_name = "form/update_form.html"


class BookLoanDeleteView(generic.edit.DeleteView):
    model = BookLoan
    success_url = "/book-loans"
    template_name = "form/delete_form.html"
