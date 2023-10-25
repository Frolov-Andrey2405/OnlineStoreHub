# from django.http import HttpResponse
from django.shortcuts import render
from .models import Product


def index(request):
    items = Product.objects.all()
    contact = {
        'items': items
    }
    return render(request, 'app/index.html', contact)


def indexItem(request, my_id):
    item = Product.objects.get(id=my_id)
    context = {
        'item': item
    }
    return render(request, 'app/detail.html', context=context)
