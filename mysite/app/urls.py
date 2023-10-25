from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('hello/', views.index),  # http://127.0.0.1:8000/hello/
    # http://127.0.0.1:8000/detail/<int:my_id>
    path('detail/<int:my_id>/', views.indexItem, name='detail'),
    path('contact/', views.contact),  # http://127.0.0.1:8000/contact/
]
