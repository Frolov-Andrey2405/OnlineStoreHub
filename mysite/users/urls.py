from django.urls import path
from .views import register

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),  # http://127.0.0.1:8000/users/
]
