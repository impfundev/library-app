from authentications.utils import Hasher
from django.shortcuts import get_object_or_404, render
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import datetime

from librarians.models import Librarians
from librarians.forms import LibrarianForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    librarians = Librarians.objects.all()
    context = {"librarians": librarians, "form": LibrarianForm()}

    default_page = 1
    page = request.GET.get("page", default_page)
    items_per_page = 5
    paginator = Paginator(librarians, items_per_page)

    try:
        page_obj = paginator.page(page)
        context["page_obj"] = page_obj
        context["librarians"] = page_obj
        cache.clear()
    except PageNotAnInteger:
        page_obj = paginator.page(default_page)
        context["page_obj"] = page_obj
        context["librarians"] = page_obj
        cache.clear()
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        context["page_obj"] = page_obj
        context["librarians"] = page_obj
        cache.clear()

    if request.method == "POST":
        form = LibrarianForm(request.POST)
        if form.is_valid:
            name = form.data["name"]
            email = form.data["email"]
            password = form.data["password"]
            hashed_password = Hasher.encode(password=password)

            Librarians.objects.create(name=name, email=email, password=hashed_password)
            cache.clear()

    if request.method == "GET":
        keyword = request.GET.get("q")
        order = request.GET.get("o")

        if keyword is not None:
            cache.clear()
            filtered_book_list = Librarians.objects.filter(
                Q(name__icontains=keyword) | Q(email__icontains=keyword)
            ).order_by("-created_at")
            context["librarians"] = filtered_book_list

        if order == "new":
            cache.clear()
            context["librarians"] = Librarians.objects.all().order_by("-updated_at")[
                :10
            ]
        elif order == "old":
            cache.clear()
            context["librarians"] = Librarians.objects.all().order_by("updated_at")

    return render(request, "librarians.html", context)


def update(request, id):
    latest_librarian_list = Librarians.objects.order_by("created_at")
    context = {"librarians": latest_librarian_list}
    librarian = Librarians.objects.get(id=id)
    initial = {
        "name": librarian.name,
        "email": librarian.email,
    }
    form = LibrarianForm(request.POST or None, initial=initial)

    if request.method == "POST":
        if form.is_valid:
            name = form.data["name"]
            email = form.data["email"]
            password = form.data["password"]
            hashed_password = Hasher.encode(password=password)
            librarian = Librarians.objects.filter(id=id)

            librarian.update(
                name=name,
                email=email,
                password=hashed_password,
                updated_at=datetime.now(),
            )
            cache.clear()
            return HttpResponseRedirect("/dashboard/librarians")

    context["form"] = form
    context["librarian_id"] = id
    return render(request, "librarians_update_form.html", context)


def delete(request, id):
    context = {}
    librarian = get_object_or_404(Librarians, id=id)

    if request.method == "POST":
        librarian.delete()
        cache.clear()
        return HttpResponseRedirect("/dashboard/librarians")

    return render(request, "librarians.html", context)
