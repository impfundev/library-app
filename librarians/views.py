from django.db.models import Q
from django.views import generic
from librarians.models import Librarians
from librarians.forms import LibrarianForm


class LibrarianListView(generic.ListView):
    model = Librarians
    template_name = "librarians.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(email__icontains=keyword)
            ).order_by("-created_at")

        if order:
            if order == "new":
                queryset = queryset.order_by("-created_at")
            elif order == "old":
                queryset = queryset.order_by("created_at")

        return queryset


class LibrarianCreateView(generic.edit.CreateView):
    model = Librarians
    form_class = LibrarianForm
    success_url = "/dashboard/librarians/"
    template_name = "form/create_form.html"
    success_message = "Librarian created successfully!"


class LibrarianUpdateView(generic.edit.UpdateView):
    model = Librarians
    form_class = LibrarianForm
    success_url = "/dashboard/librarians"
    template_name = "form/update_form.html"
    success_message = "Librarian updated successfully!"


class LibrarianDeleteView(generic.edit.DeleteView):
    model = Librarians
    success_url = "/dashboard/librarians"
    template_name = "form/delete_form.html"
    success_message = "Librarian deleted successfully!"
