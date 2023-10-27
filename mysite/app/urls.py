from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),  # http://127.0.0.1:8000/
    path('detail/<int:my_id>/', views.indexItem, name='detail'),  # http://127.0.0.1:8000/detail/<int:my_id>
    path('add_item/', views.add_item, name='add_item'),  # http://127.0.0.1:8000/add_item/
    path("update_item/<int:my_id>/", views.update_item, name="update_item"),  # http://127.0.0.1:8000/update_item/<int:my_id>
    path("delete_item/<int:my_id>/", views.delete_item, name="delete_item"),  # http://127.0.0.1:8000/delete_item/<int:my_id>
]
