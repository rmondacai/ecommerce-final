from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm, RegistroForm


def producto_list(request):
    """Catálogo público de productos."""
    productos = Producto.objects.filter(disponible=True).select_related('categoria')
    categorias = Categoria.objects.filter(activa=True)

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    paginator = Paginator(productos, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'catalogo/producto_list.html', {
        'page_obj': page_obj,
        'categorias': categorias,
        'categoria_actual': categoria_id,
    })


def producto_detail(request, pk):
    """Detalle de un producto."""
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'catalogo/producto_detail.html', {'producto': producto})


@staff_member_required
def producto_create(request):
    """Crear producto (solo admin)."""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('catalogo:producto_list')
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ProductoForm()
    return render(request, 'catalogo/producto_form.html', {'form': form, 'titulo': 'Crear Producto'})


@staff_member_required
def producto_update(request, pk):
    """Editar producto (solo admin)."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('catalogo:producto_detail', pk=producto.pk)
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'catalogo/producto_form.html', {'form': form, 'titulo': 'Editar Producto', 'producto': producto})


@staff_member_required
def producto_delete(request, pk):
    """Eliminar producto (solo admin)."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado.')
        return redirect('catalogo:producto_list')
    return render(request, 'catalogo/producto_confirm_delete.html', {'producto': producto})


@staff_member_required
def admin_productos(request):
    """Panel de administración de productos (solo admin)."""
    productos = Producto.objects.select_related('categoria').all()
    return render(request, 'catalogo/admin_productos.html', {'productos': productos})


def registro_usuario(request):
    """Registro de nuevo usuario (cliente)."""
    if request.user.is_authenticated:
        return redirect('catalogo:producto_list')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenido/a {user.first_name}. Tu cuenta fue creada correctamente.')
            return redirect('catalogo:producto_list')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})
