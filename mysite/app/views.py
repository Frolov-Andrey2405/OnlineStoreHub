from django.shortcuts import render
from .models import Product


def index(request):
    items = Product.objects.all()
    contact = {
        'items': items
    }
    return render(request, 'app/index.html', contact)


def contact(request):
    return render(request, 'app/contacts.html')
