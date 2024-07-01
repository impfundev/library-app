from django.urls import path
from authentications.views import AuthView

urlpatterns = [
    path("login/", AuthView.login, name="login"),
    path("sign-up/", AuthView.sign_up, name="sign_up"),
    path("logout/", AuthView.logout, name="logout"),
    path("forgot-password/", AuthView.forgot_password, name="forgot_password"),
]
