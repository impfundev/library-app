from django.db.models import Q
from django.views import generic

from .models import Book
from .forms import BookForm


class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(category__name__icontains=keyword)
                | Q(publish_date__year__icontains=keyword)
            ).order_by("-created_at")

        if order:
            if order == "new":
                queryset = queryset.order_by("-created_at")
            elif order == "old":
                queryset = queryset.order_by("created_at")

        return queryset.order_by("-created_at")


class BookDetailView(generic.DeleteView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"


class BookCreateView(generic.edit.CreateView):
    model = Book
    form_class = BookForm
    success_url = "/dashboard/books/"
    template_name = "form/create_form.html"


class BookUpdateView(generic.edit.UpdateView):
    model = Book
    form_class = BookForm
    success_url = "/dashboard/books"
    template_name = "form/update_form.html"


class BookDeleteView(generic.edit.DeleteView):
    model = Book
    success_url = "/dashboard/books"
    template_name = "form/delete_form.html"
