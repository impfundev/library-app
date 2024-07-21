from django.db.models import Q
from django.views import generic
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from users.models import Librarian, Member, LibrarianLoginHistory
from users.forms import UserForm, User, LoginForm, SignUpForm, ForgotPasswordForm


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
    paginate_by = 10


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
    success_url = "/users/librarians"


class LibrarianDeleteView(UserDeleteView):
    model = Librarian
    success_url = "/users/librarians"


class MemberListView(UserListView):
    model = Member
    template_name = "members/members.html"
    paginate_by = 10


class MemberCreateView(UserCreateView):
    model = User
    success_url = "/users/members/"

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
    success_url = "/users/members"


class MemberDeleteView(UserDeleteView):
    model = Member
    success_url = "/users/members"


class LibrarianLoginView(LoginView):
    form_class = LoginForm
    template_name = "librarians/login.html"
    redirect_authenticated_user = "/dashboard/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data()

        if form.is_valid():
            username = form.data.get("username")
            user = User.objects.get(username=username)

            if not user.is_staff:
                context["error_message"] = "Access Denied, account is not staff"

                return self.form_invalid(form)

            librarian = Librarian.objects.get(user=user)
            LibrarianLoginHistory.objects.create(librarian=librarian)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LibrarianLogoutView(generic.TemplateView):
    success_url = "/users/auth/login/"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect(self.success_url)

        return self.render_to_response(context)


class LibrarianSignUpView(generic.FormView):
    form_class = SignUpForm
    template_name = "librarians/sign_up.html"
    success_url = "/users/auth/login/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid:
            context = self.get_context_data()
            username = form.data.get("username")
            email = form.data.get("email")
            password1 = form.data.get("password1")
            password2 = form.data.get("password2")

            is_password_confirmed = password1 != password2
            if is_password_confirmed:
                return self.form_invalid(form)

            is_email = User.objects.filter(email=email)
            if is_email.exists():
                return self.form_invalid(form)

            user = User.objects.create_user(
                username=username, email=email, is_staff=True
            )
            user.set_password(password1)
            user.save()

            Librarian.objects.create(user=user)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LibrarianResetPassword(SuccessMessageMixin, PasswordResetView):
    form_class = ForgotPasswordForm
    template_name = "password/password_reset.html"
    email_template_name = "password/password_reset_email.html"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = "/password-reset-complete/"


class LibrarianLoginHistoryView(generic.ListView):
    model = LibrarianLoginHistory
    template_name = "librarians/librarian_login_history.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("q")
        order = self.request.GET.get("o")

        if keyword:
            queryset = queryset.filter(
                Q(librarian__user__username__icontains=keyword)
                | Q(librarian__user__email__icontains=keyword)
            ).order_by("-date")

        if order:
            if order == "new":
                queryset = queryset.order_by("-date")
            elif order == "old":
                queryset = queryset.order_by("date")

        return queryset.order_by("-date")
