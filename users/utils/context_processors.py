from ..models import Librarian


def user_context(request):
    user = request.user
    librarian = Librarian.objects.get(user=user)

    return {"user": user, "librarian_id": librarian.id}
