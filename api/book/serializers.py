from rest_framework import serializers

from book.models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    category = Category

    class Meta:
        model = Book
        fields = "__all__"
