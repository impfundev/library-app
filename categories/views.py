from django.db.models import Q
from django.views import generic
from categories.models import Category
from categories.forms import CategoryForm


class CategoryListView(generic.ListView):
    model = Category
    template_name = "categories.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
            ).order_by("-created_at")

        if order:
            if order == "new":
                queryset = queryset.order_by("-created_at")
            elif order == "old":
                queryset = queryset.order_by("created_at")

        return queryset.order_by("-updated_at")


class CategoryCreateView(generic.edit.CreateView):
    model = Category
    form_class = CategoryForm
    success_url = "/dashboard/categories/"
    template_name = "form/create_form.html"


class CategoryUpdateView(generic.edit.UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = "/dashboard/categories/"
    template_name = "form/update_form.html"


class CategoryDeleteView(generic.edit.DeleteView):
    model = Category
    success_url = "/dashboard/categories/"
    template_name = "form/delete_form.html"
