from django.shortcuts import render


def home(request):
    return render(request, "homepage.html")


def index(request):
    return render(request, "dashboard/index.html")
