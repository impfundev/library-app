from django.urls import path
from authentications.views import login, sign_up

urlpatterns = [
    path("login/", login, name="login"),
    path("sign-up/", sign_up, name="sign_up"),
]
