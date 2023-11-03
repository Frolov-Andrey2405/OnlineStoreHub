import json
import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import DeleteView


from .models import OrderDetail, Product


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
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["stripe_publishable_key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


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


@csrf_exempt
def create_checkout_session(request, id):
    product = get_object_or_404(Product, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("app:success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("app:failed")),
    )
    order = OrderDetail()
    order.product = product
    order.stripe_payment_intent = checkout_session["payment_intent"]
    order.amount = int(product.price * 100)
    order.save()
    return JsonResponse({"sessionId": checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "app/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if session_id is None:
            return HttpResponseNotFound()
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        order = get_object_or_404(
            OrderDetail, stripe_payment_intent=session.payment_intent
        )
        order.has_paid = True
        order.save()
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):
    template_name = "app/payment_failed.html"
