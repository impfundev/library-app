import jwt

from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from librarians.models import Librarians
from django.conf import settings


class AuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        auth_session = request.session.get("auth_session", None)

        if request.path.startswith("/dashboard/"):
            if auth_session is not None:
                decoded = jwt.decode(
                    auth_session, settings.JWT_SECRET, algorithms=["HS256"]
                )
                user_verified = get_object_or_404(
                    Librarians, id=decoded["librarian_id"]
                )

                user_obj = {
                    "exp": decoded["exp"],
                    "id": user_verified.id,
                    "name": user_verified.name,
                    "time": str(datetime.now()),
                }
                message = "login request success, user: " + f"{user_obj}"
                print(message)

                return response
            else:
                return HttpResponseRedirect("/auth/login")

        if auth_session is not None and request.path.startswith("/auth/"):
            return HttpResponseRedirect("/dashboard/")
        else:
            return response
