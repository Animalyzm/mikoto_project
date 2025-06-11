from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("<h1>Welcome to Django!</h1>")


def temp_test(request):
    return render(request, 'temp_test.html', context={})
