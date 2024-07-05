from django.shortcuts import get_object_or_404, render
from django.core.cache import cache
from django.http import HttpResponseRedirect
from datetime import datetime
from django.db.models import Q

from books.models import Book
from books.forms import BookForm


def index(request):
    context = {"form": BookForm()}
    latest_book_list = Book.objects.order_by("-created_at")[:10]
    context["books"] = latest_book_list

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid:
            title = form.data["title"]
            stock = form.data["stock"]
            description = form.data["description"]

            Book.objects.create(title=title, stock=stock, description=description)
            cache.clear()

    if request.method == "GET":
        query = request.GET.get("q")
        order = request.GET.get("o")

        if query is not None:
            cache.clear()
            filtered_book_list = Book.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by("-created_at")[:10]
            context["books"] = filtered_book_list

        if order == "new":
            cache.clear()
            context["books"] = Book.objects.all().order_by("-updated_at")[:10]
        elif order == "old":
            cache.clear()
            context["books"] = Book.objects.all().order_by("updated_at")[:10]

    return render(request, "book.html", context)


def update(request, id):
    latest_book_list = Book.objects.order_by("created_at")[:10]
    context = {"books": latest_book_list}
    book = Book.objects.get(id=id)
    initial_dict = {
        "title": book.title,
        "stock": book.stock,
        "description": book.description,
    }
    print(book.title)
    form = BookForm(request.POST or None, initial=initial_dict)

    if request.method == "POST":
        if form.is_valid:
            title = form.data["title"]
            stock = form.data["stock"]
            description = form.data["description"]
            book = Book.objects.filter(id=id)

            book.update(
                title=title,
                stock=stock,
                description=description,
                updated_at=datetime.now(),
            )
            cache.clear()
            return HttpResponseRedirect("/dashboard/books")

    context["form"] = form
    context["book_id"] = id
    return render(request, "book_update_form.html", context)


def delete(request, id):
    context = {}
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        book.delete()
        cache.clear()
        return HttpResponseRedirect("/dashboard/books")

    return render(request, "book.html", context)
