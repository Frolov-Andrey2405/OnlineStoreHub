from django.urls import path
from app import views

urlpatterns = [
    path('hello/', views.index),  # http://127.0.0.1:8000/hello/
    path('detail/<int:my_id>/', views.indexItem),  # http://127.0.0.1:8000/hello/<int:my_id>
    path('contact/', views.contact),  # http://127.0.0.1:8000/contact/
]
