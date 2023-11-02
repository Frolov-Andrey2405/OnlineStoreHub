from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


def index(request):
    page_obj = items = Product.objects.all()

    item_name = request.GET.get('search')
    if item_name != '' and item_name is not None:
        page_obj = items.filter(name__icontains=item_name)

    paginator = Paginator(page_obj, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, "app/index.html", context)


class ProductListView(ListView):
    model = Product
    template_name = "app/index.html"
    context_object_name = "items"
    paginate_by = 2


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
