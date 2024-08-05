from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from book.models import Book, Category
from .serializers import BookSerializer, CategorySerializer


@csrf_exempt
def bookView(request):
    books = Book.objects.all().order_by("created_at")
    category = request.GET.get("category")
    keyword = request.GET.get("search")

    if request.method == "GET":
        if category:
            books = books.filter(category__name=category)

        if keyword and len(keyword) >= 3:
            books = books.filter(title__icontains=keyword)

        data = []
        for book_item in books:
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
        return JsonResponse(data, status=200, safe=False)

    return JsonResponse({"message": "Invalid request method"}, status=405)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("created_at")
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category__name"]
    search_fields = ["title"]

    def get_queryset(self):
        year = self.request.query_params.get("year")
        queryset = self.queryset

        if year is not None:
            return queryset.filter(publish_date__year=year)

        return queryset

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("created_at")
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["created_at", "updated_at"]
    search_fields = ["name"]

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
