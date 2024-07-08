from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from api.serializers import get_user_model, UserSerializer


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all().order_by("id")
    serializer_class = UserSerializer
