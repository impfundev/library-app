from django.db.models import Q
from django.views import generic

from .forms import Book, BookForm, Category, CategoryForm


class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    paginate_by = 10

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
    success_url = "/books/"
    template_name = "form/create_form.html"


class BookUpdateView(generic.edit.UpdateView):
    model = Book
    form_class = BookForm
    success_url = "/books"
    template_name = "form/update_form.html"


class BookDeleteView(generic.edit.DeleteView):
    model = Book
    success_url = "/books"
    template_name = "form/delete_form.html"


class CategoryListView(generic.ListView):
    model = Category
    template_name = "categories.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword)).order_by(
                "-created_at"
            )

        if order:
            if order == "new":
                queryset = queryset.order_by("-created_at")
            elif order == "old":
                queryset = queryset.order_by("created_at")

        return queryset.order_by("-updated_at")


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context["object"] = self.object
            context_object_name = self.get_context_object_name(self.object)
            books = Book.objects.filter(category=self.object.id)
            context["object_list"] = books
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)


class CategoryCreateView(generic.edit.CreateView):
    model = Category
    form_class = CategoryForm
    success_url = "/books/categories/"
    template_name = "form/create_form.html"


class CategoryUpdateView(generic.edit.UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = "/books/categories/"
    template_name = "form/update_form.html"


class CategoryDeleteView(generic.edit.DeleteView):
    model = Category
    success_url = "/books/categories/"
    template_name = "form/delete_form.html"
