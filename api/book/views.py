from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from book.models import Book, Category


@csrf_exempt
def bookView(request):
    books = Book.objects.all().order_by("created_at")
    category = request.GET.get("category")
    keyword = request.GET.get("search")
    page_number = request.GET.get("page", 1)

    if request.method == "GET":
        if category:
            books = books.filter(category__name=category)

        if keyword and len(keyword) >= 3:
            books = books.filter(title__icontains=keyword)

        paginator = Paginator(books, 10)
        page_obj = paginator.get_page(page_number)

        data = []
        for book_item in page_obj:
            if book_item.category is not None:
                book = {
                    "id": book_item.id,
                    "title": book_item.title,
                    "author": book_item.author,
                    "description": book_item.description,
                    "cover_image": "http://127.0.0.1:8000" + book_item.cover_image.url,
                    "category": {
                        "name": book_item.category.name,
                    },
                }

            book = {
                "id": book_item.id,
                "title": book_item.title,
                "author": book_item.author,
                "description": book_item.description,
                "cover_image": "http://127.0.0.1:8000" + book_item.cover_image.url,
            }
            data.append(book)

        response_data = {
            "data": data,
            "has_next": page_obj.has_next(),
            "has_prev": page_obj.has_previous(),
            "page_number": page_obj.number,
            "total_pages": paginator.num_pages,
        }

        return JsonResponse(response_data, status=200, safe=False)

    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def categoryView(request):
    categories = Category.objects.all().order_by("created_at")

    if request.method == "GET":
        data = []
        for category_item in categories:
            category = {
                "id": category_item.id,
                "name": category_item.name,
            }
            data.append(category)

        return JsonResponse(data, safe=False, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)
