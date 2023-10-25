from django.urls import path
from app import views

urlpatterns = [
    path('hello/', views.index),  # http://127.0.0.1:8000/hello/
    path('hello/<int:id>/', views.indexItem),  # http://127.0.0.1:8000/hello/<int:id>
    path('contact/', views.contact),  # http://127.0.0.1:8000/contact/
]
