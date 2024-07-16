from ..models import Librarian


def user_context(request):
    if request.user.is_authenticated:
        user = request.user
        librarian = Librarian.objects.get(user=user)
        return {"user": user, "librarian_id": librarian.id}

    return {"user": None, "librarian_id": None}
