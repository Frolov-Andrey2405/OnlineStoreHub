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


def add_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES['upload']
        item = Product(
            name=name, price=price, description=description, image=image)
        item.save()
    return render(request, 'app/add_item.html')
