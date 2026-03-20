from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from catalogo.models import Producto
from .carrito import Carrito


@login_required
def carrito_detalle(request):
    """Muestra el contenido del carrito."""
    carrito = Carrito(request)
    items = carrito.get_items()
    total = carrito.get_total()
    return render(request, 'carrito/detalle.html', {'items': items, 'total': total})


@login_required
def carrito_agregar(request, producto_id):
    """Agrega un producto al carrito."""
    producto = get_object_or_404(Producto, id=producto_id, disponible=True)
    carrito = Carrito(request)

    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad < 1:
        cantidad = 1

    if cantidad > producto.stock:
        messages.warning(request, f'Solo hay {producto.stock} unidades disponibles de "{producto.nombre}".')
        return redirect('catalogo:producto_detail', pk=producto.id)

    carrito.agregar(producto, cantidad)
    messages.success(request, f'"{producto.nombre}" agregado al carrito.')
    return redirect('carrito:detalle')


@login_required
def carrito_quitar(request, producto_id):
    """Elimina un producto del carrito."""
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = Carrito(request)
    carrito.quitar(producto)
    messages.info(request, f'"{producto.nombre}" eliminado del carrito.')
    return redirect('carrito:detalle')


@login_required
def carrito_actualizar(request, producto_id):
    """Actualiza la cantidad de un producto en el carrito."""
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = Carrito(request)

    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad > producto.stock:
        messages.warning(request, f'Solo hay {producto.stock} unidades disponibles.')
        cantidad = producto.stock

    if cantidad < 1:
        carrito.quitar(producto)
        messages.info(request, f'"{producto.nombre}" eliminado del carrito.')
    else:
        carrito.actualizar_cantidad(producto, cantidad)
        messages.success(request, 'Cantidad actualizada.')

    return redirect('carrito:detalle')
