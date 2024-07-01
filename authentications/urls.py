from django.urls import path
from authentications.views import login, sign_up, logout

urlpatterns = [
    path("login/", login, name="login"),
    path("sign-up/", sign_up, name="sign_up"),
    path("logout/", logout, name="logout"),
]
