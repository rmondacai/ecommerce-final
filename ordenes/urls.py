from django.urls import path
from . import views

app_name = 'ordenes'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion/<int:orden_id>/', views.confirmacion, name='confirmacion'),
    path('mis-ordenes/', views.mis_ordenes, name='mis_ordenes'),
]
