import jwt
from django.shortcuts import render


def home(request):
    return render(request, "homepage.html")


def index(request):
    auth_session = request.session["auth_session"]
    decoded = jwt.decode(auth_session, "secret", algorithms=["HS256"])
    print(decoded)
    context = {"user_session": decoded}

    return render(request, "dashboard/index.html", context)
