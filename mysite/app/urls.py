from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),  # http://127.0.0.1:8000/
    path('detail/<int:my_id>/', views.indexItem, name='detail'),  # http://127.0.0.1:8000/detail/<int:my_id>
    path('add_item/', views.add_item, name='add_item'),  # http://127.0.0.1:8000/add_item/
]
