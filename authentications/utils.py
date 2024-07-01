import jwt
from django.conf import settings


def create_auth_session(request, payload):
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    request.session["auth_session"] = token
