from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from catalogo.views import registro_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalogo.urls')),
    path('carrito/', include('carrito.urls')),
    path('ordenes/', include('ordenes.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', registro_usuario, name='registro'),
]
