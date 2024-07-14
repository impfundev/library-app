from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import Book, BookSerializer, Category, CategorySerializer


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
