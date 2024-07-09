from django.db.models import Q
from django.views import generic
from members.models import Members
from members.forms import MemberForm


class MemberListView(generic.ListView):
    model = Members
    template_name = "members.html"
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

        return queryset.order_by("-updated_at")


class MemberCreateView(generic.edit.CreateView):
    model = Members
    form_class = MemberForm
    success_url = "/dashboard/members/"
    template_name = "form/create_form.html"


class MemberUpdateView(generic.edit.UpdateView):
    model = Members
    form_class = MemberForm
    success_url = "/dashboard/members"
    template_name = "form/update_form.html"


class MemberDeleteView(generic.edit.DeleteView):
    model = Members
    success_url = "/dashboard/members"
    template_name = "form/delete_form.html"
