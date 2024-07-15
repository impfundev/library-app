from django.db.models import Q
from django.views import generic

from users.models import Librarian, Member
from users.forms import UserForm, User


class UserListView(generic.ListView):

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        if keyword:
            queryset = queryset.filter(
                Q(user__name__icontains=keyword) | Q(user__email__icontains=keyword)
            ).order_by("-created_at")

        if order:
            if order == "new":
                queryset = queryset.order_by("-created_at")
            elif order == "old":
                queryset = queryset.order_by("created_at")

        return queryset.order_by("-updated_at")


class UserCreateView(generic.FormView):
    form_class = UserForm
    template_name = "form/create_form.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            formData = form.cleaned_data.copy()
            user = self.model.objects.create_user(**formData, is_staff=True)

            return user
        else:
            return None


class UserUpdateView(generic.FormView):
    form_class = UserForm
    template_name = "form/update_form.html"

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=kwargs["pk"])
        self.initial = {
            "username": obj.user.username,
            "email": obj.user.email,
            "password": obj.user.password,
        }

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=kwargs["pk"])
        form = self.get_form()

        if form.is_valid():
            formData = form.cleaned_data.copy()
            User.objects.filter(pk=obj.user.id).update(**formData)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserDeleteView(generic.edit.DeleteView):
    template_name = "form/delete_form.html"

    def form_valid(self, form):
        user_pk = self.get_object().user.id
        User.objects.get(pk=user_pk).delete()
        return super().form_valid(form)


class LibrarianListView(UserListView):
    model = Librarian
    template_name = "librarians/librarians.html"
    paginate_by = 5


class LibrarianCreateView(UserCreateView):
    model = User
    success_url = "/dashboard/librarians/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = super().post(request)
            Librarian.objects.create(user=user)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LibrarianUpdateView(UserUpdateView):
    model = Librarian
    success_url = "/dashboard/librarians"


class LibrarianDeleteView(UserDeleteView):
    model = Librarian
    success_url = "/dashboard/librarians"


class MemberListView(UserListView):
    model = Member
    template_name = "members/members.html"
    paginate_by = 5


class MemberCreateView(UserCreateView):
    model = User
    success_url = "/dashboard/members/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = super().post(request)
            Member.objects.create(user=user)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MemberUpdateView(UserUpdateView):
    model = Member
    success_url = "/dashboard/members"


class MemberDeleteView(UserDeleteView):
    model = Member
    success_url = "/dashboard/members"
