from django.db.models import Q
from django.views import generic

from members.models import Members
from members.forms import MemberForm
from authentications.utils import Hasher


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


class MemberCreateView(generic.FormView):
    model = Members
    form_class = MemberForm
    success_url = "/dashboard/members/"
    template_name = "form/create_form.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            formData = form.cleaned_data.copy()
            formData["password"] = Hasher.encode(formData["password"])
            self.model.objects.create(**formData)

        return super().post(request, *args, **kwargs)


class MemberUpdateView(generic.FormView):
    model = Members
    form_class = MemberForm
    success_url = "/dashboard/members"
    template_name = "form/update_form.html"

    def get(self, request, *args, **kwargs):
        member = self.model.objects.get(pk=kwargs["pk"])
        self.initial = {
            "name": member.name,
            "email": member.email,
            "password": member.password,
        }

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        member = self.model.objects.get(pk=kwargs["pk"])
        form = self.get_form()

        if form.is_valid():
            formData = form.cleaned_data.copy()
            new_password = form.cleaned_data.get("password")

            if new_password:
                formData["password"] = Hasher.encode(formData["password"])
            else:
                formData["password"] = member.password

            self.model.objects.filter(pk=kwargs["pk"]).update(**formData)

            return super().post(request, *args, **kwargs)

        return self.form_invalid(form)


class MemberDeleteView(generic.edit.DeleteView):
    model = Members
    success_url = "/dashboard/members"
    template_name = "form/delete_form.html"
