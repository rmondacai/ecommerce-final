from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.producto_list, name='producto_list'),
    path('producto/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('producto/crear/', views.producto_create, name='producto_create'),
    path('producto/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('producto/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),
    path('admin-productos/', views.admin_productos, name='admin_productos'),
]
