import jwt
import bcrypt
from django.conf import settings


def create_auth_session(request, payload):
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    request.session["auth_session"] = token


class Hasher:
    def encode(password: str):
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt(rounds=8)
        )
        return hashed_password

    def verify(password: str, encoded: str):
        hashed_password = encoded[2:].replace("'", "").encode("utf-8")
        password_encode = password.encode("utf-8")

        print(hashed_password)
        print(password_encode)

        is_verified = bcrypt.checkpw(
            password=password_encode, hashed_password=hashed_password
        )

        return is_verified
