from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from datetime import datetime

from librarians.models import Librarians
from librarians.forms import LibrarianForm


def index(request):
    latest_librarian_list = Librarians.objects.order_by("created_at")[:10]
    context = {"librarians": latest_librarian_list, "form": LibrarianForm()}

    if request.method == "POST":
        form = LibrarianForm(request.POST)
        if form.is_valid:
            name = form.data["name"]
            email = form.data["email"]
            password = form.data["password"]

            Librarians.objects.create(name=name, email=email, password=password)

    return render(request, "librarians.html", context)


def update(request, id):
    latest_librarian_list = Librarians.objects.order_by("created_at")[:10]
    context = {"librarians": latest_librarian_list}
    librarian = Librarians.objects.get(id=id)
    initial = {
        "name": librarian.name,
        "email": librarian.email,
        "password": librarian.password,
    }
    form = LibrarianForm(request.POST or None, initial=initial)

    if request.method == "POST":
        if form.is_valid:
            name = form.data["name"]
            email = form.data["email"]
            password = form.data["password"]
            librarian = Librarians.objects.filter(id=id)

            librarian.update(
                name=name, email=email, password=password, updated_at=datetime.now()
            )
            return HttpResponseRedirect("/dashboard/librarians")

    context["form"] = form
    context["librarian_id"] = id
    return render(request, "librarians_update_form.html", context)


def delete(request, id):
    context = {}
    librarian = get_object_or_404(Librarians, id=id)

    if request.method == "POST":
        librarian.delete()
        return HttpResponseRedirect("/dashboard/librarians")

    return render(request, "librarians.html", context)
