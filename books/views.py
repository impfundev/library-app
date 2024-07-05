from django.shortcuts import get_object_or_404, render
from django.core.cache import cache

from django.http import HttpResponseRedirect
from datetime import datetime
from django.db.models import Q

from books.models import Book
from books.forms import BookForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    context = {"form": BookForm()}
    books = Book.objects.all()

    default_page = 1
    page = request.GET.get("page", default_page)
    items_per_page = 5
    paginator = Paginator(books, items_per_page)

    try:
        page_obj = paginator.page(page)
        context["page_obj"] = page_obj
        context["books"] = page_obj
        cache.clear()
    except PageNotAnInteger:
        page_obj = paginator.page(default_page)
        context["page_obj"] = page_obj
        context["books"] = page_obj
        cache.clear()
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        context["page_obj"] = page_obj
        context["books"] = page_obj
        cache.clear()

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid:
            title = form.data["title"]
            stock = form.data["stock"]
            description = form.data["description"]

            Book.objects.create(title=title, stock=stock, description=description)
            cache.clear()

    if request.method == "GET":
        keyword = request.GET.get("q")
        order = request.GET.get("o")

        if keyword is not None:
            cache.clear()
            filtered_book_list = Book.objects.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            ).order_by("-created_at")
            context["books"] = filtered_book_list

        if order == "new":
            cache.clear()
            context["books"] = Book.objects.all().order_by("-updated_at")
        elif order == "old":
            cache.clear()
            context["books"] = Book.objects.all().order_by("updated_at")

    return render(request, "book.html", context)


def update(request, id):
    latest_book_list = Book.objects.order_by("created_at")
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
