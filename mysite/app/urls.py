from django.urls import path

from app.views import (
    ProductDeleteView,  # ProductListView,
    ProductDetailView,
    PaymentSuccessView, PaymentFailedView,
    add_item, index, 
    update_item)

app_name = "app"

urlpatterns = [
    # http://127.0.0.1:8000/
    path("", index, name='index'),
    # path("", ProductListView.as_view(), name="index"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("add_item/", add_item, name="add_item"),
    path("update_item/<int:my_id>/", update_item, name="update_item"),
    path("delete_item/<int:pk>/", ProductDeleteView.as_view(), name="delete_item"),
    path("success/", PaymentSuccessView.as_view(), name="success"),
    path("failed/", PaymentFailedView.as_view(), name="failed"),
    path("api/checkout-session/<int:id>/", update_item, name="api_checkout_session"),
]
