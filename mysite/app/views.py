# from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Index")


def contact(request):
    return HttpResponse("Contacts")
