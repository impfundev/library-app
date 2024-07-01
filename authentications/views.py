from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from authentications.forms import LoginForm, SignUpForm, ForgotPassword
from librarians.models import Librarians, LoginHistory
from authentications.utils import create_auth_session


class AuthView(TemplateView):
    def login(request):
        librarian = Librarians.objects.all()
        context = {"form": LoginForm()}
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                account = librarian.filter(
                    email=form.data["email"], password=form.data["password"]
                )

                if account.exists():
                    librarian = librarian.get(
                        email=form.data["email"],
                        password=form.data["password"],
                    )
                    payload = {
                        "librarian_id": librarian.id,
                        "name": librarian.name,
                        "email": librarian.email,
                    }

                    create_auth_session(request, payload)

                    LoginHistory.objects.create(librarian_id=librarian.id)
                    return HttpResponseRedirect("/dashboard/")
                else:
                    context["error_message"] = (
                        "Email or Password invalid, please enter valid data or Sign Up first"
                    )
        else:
            form = LoginForm()

        return render(request, "login.html", context)

    def sign_up(request):
        librarian = Librarians.objects.all()
        context = {"form": SignUpForm()}
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                is_email = librarian.filter(email=form.data["email"])

                if is_email.exists():
                    context["error_message"] = (
                        "Email was already exist, please use different email"
                    )
                else:
                    librarian.create(
                        name=form.data["name"],
                        email=form.data["email"],
                        password=form.data["password"],
                    )
                    new_librarian = librarian.get(
                        name=form.data["name"],
                        email=form.data["email"],
                        password=form.data["password"],
                    )

                    payload = {
                        "librarian_id": new_librarian.id,
                        "name": new_librarian.name,
                        "email": new_librarian.email,
                    }
                    create_auth_session(request, payload)

                    LoginHistory.objects.create(librarian_id=new_librarian.id)
                    return HttpResponseRedirect("/dashboard/")
        else:
            form = SignUpForm()

        return render(request, "sign_up.html", context)

    def logout(request):
        del request.session["auth_session"]
        return HttpResponseRedirect("/auth/login")

    def forgot_password(request):
        librarian = Librarians.objects.all()
        context = {"form": ForgotPassword()}

        if request.method == "POST":
            form = ForgotPassword(request.POST)
            if form.is_valid:
                account = librarian.filter(
                    email=form.data["email"], password=form.data["old_password"]
                )

                if account.exists():
                    if form.data["old_password"] == form.data["new_password"]:
                        context["error_message"] = (
                            "Old and New password cannot be same!"
                        )
                    else:
                        try:
                            librarian.update(password=form.data["new_password"])
                            context["message"] = (
                                "Change password success, now lets try login!"
                            )
                        except:
                            context["error_message"] = (
                                "Change password failed, please try again later."
                            )
                else:
                    context["error_message"] = (
                        "Account with email and old password not found, please enter valid data!"
                    )

        return render(request, "forgot-password.html", context)
