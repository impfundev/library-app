"""
URL configuration for library_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from dashboards.views import HomePage

urlpatterns = [
    path("", HomePage.as_view(), name="homepage"),
    path("dashboard/", include("dashboards.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("authentications.urls")),
    # API
    path("api/v1/", include("api.urls")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path(
        "api/v1/auth/registration/",
        include("dj_rest_auth.registration.urls"),
        name="register",
    ),
    path("api-auth/", include("rest_framework.urls")),
]
