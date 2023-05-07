from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    return render(request, 'assistant/home.html')


def error_handler(request):
    return render(request, 'assistant/404.html')