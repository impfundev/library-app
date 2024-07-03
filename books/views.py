from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from datetime import datetime

from books.models import Book
from books.forms import BookForm


def index(request):
    latest_book_list = Book.objects.order_by("created_at")[:10]
    context = {"books": latest_book_list, "form": BookForm()}

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid:
            title = form.data["title"]
            stock = form.data["stock"]
            description = form.data["description"]

            Book.objects.create(title=title, stock=stock, description=description)

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
            return HttpResponseRedirect("/dashboard/books")

    context["form"] = form
    context["book_id"] = id
    return render(request, "book_update_form.html", context)


def delete(request, id):
    context = {}
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        book.delete()
        return HttpResponseRedirect("/dashboard/books")

    return render(request, "book.html", context)
