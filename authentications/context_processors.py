import jwt
from django.shortcuts import get_object_or_404
from librarians.models import Librarians
from django.conf import settings


def get_auth_session(request):
    auth_session = request.session.get("auth_session", None)

    if auth_session:
        decoded = jwt.decode(auth_session, settings.JWT_SECRET, algorithms=["HS256"])

        user_id = decoded["librarian_id"]
        user_verified = get_object_or_404(Librarians, id=user_id)

        return {"user": user_verified}

    return {"user": None}
