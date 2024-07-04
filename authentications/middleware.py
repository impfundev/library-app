import jwt

from django.conf import settings
from datetime import datetime, timedelta
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
import jwt.utils


class AuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        auth_session = request.session.get("auth_session", None)

        if auth_session is not None:
            try:
                payload = jwt.decode(
                    auth_session, settings.JWT_SECRET, algorithms=["HS256"]
                )

                # refresh token 5 minutes before expired
                expired_time = datetime.fromtimestamp(payload["exp"])
                near_expired = expired_time - timedelta(minutes=5)

                if datetime.now() >= near_expired:
                    payload["exp"] = payload["exp"] + timedelta(hours=2).total_seconds()
                    new_token = jwt.encode(
                        payload, settings.JWT_SECRET, algorithm="HS256"
                    )
                    request.session["auth_session"] = new_token

                return response

            except jwt.ExpiredSignatureError:
                del request.session["auth_session"]
                return HttpResponseRedirect("/auth/login")

        if auth_session is None and request.path.startswith("/dashboard/"):
            return HttpResponseRedirect("/auth/login")
        elif auth_session is not None and request.path.startswith("/auth/"):
            return HttpResponseRedirect("/dashboard/")
        else:
            return response
