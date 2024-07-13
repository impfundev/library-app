from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .serializers import Librarian, LibrarianSerializer, Member, MemberSerializer


class LibrarianViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Librarian.objects.all().order_by("created_at")
    serializer_class = LibrarianSerializer

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Member.objects.all().order_by("created_at")
    serializer_class = MemberSerializer

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
