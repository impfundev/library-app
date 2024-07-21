from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect


class AuthMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated and request.path.startswith("/dashboard/"):
            return HttpResponseRedirect("/users/auth/login")
        elif request.user.is_authenticated and request.path.startswith("/users/auth/"):
            return HttpResponseRedirect("/dashboard/")
        else:
            return response
