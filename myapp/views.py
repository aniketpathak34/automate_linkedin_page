from django.http import HttpResponse
import os

def home(request):
    return HttpResponse("Hello, Dockerized Django!")

def test(request):
    pass