from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product
    template_name = "app/index.html"
    context_object_name = "items"


class ProductDetailView(DetailView):
    model = Product
    template_name = "app/detail.html"
    context_object_name = "item"


@login_required
def add_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES['upload']
        seller = request.user
        item = Product(
            name=name, price=price, description=description,
            image=image, seller=seller)
        item.save()
    return render(request, 'app/add_item.html')


def update_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.image = request.FILES.get('upload', item.image)
        item.save()
        return redirect("/")
    context = {"item": item}
    return render(request, "app/update_item.html", context)


def delete_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.delete()
        return redirect("/")
    context = {"item": item}
    return render(request, "app/delete_item.html", context)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("app:index")
