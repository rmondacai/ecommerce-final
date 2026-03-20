from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.carrito_detalle, name='detalle'),
    path('agregar/<int:producto_id>/', views.carrito_agregar, name='agregar'),
    path('quitar/<int:producto_id>/', views.carrito_quitar, name='quitar'),
    path('actualizar/<int:producto_id>/', views.carrito_actualizar, name='actualizar'),
]
