from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def index(request):
    items = Product.objects.all()
    return HttpResponse(items)


def contact(request):
    return render(request, 'app/contacts.html')
