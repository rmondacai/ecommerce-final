from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from carrito.carrito import Carrito
from .models import Orden, OrdenItem


@login_required
def checkout(request):
    """Muestra resumen del carrito y permite confirmar la compra."""
    carrito = Carrito(request)
    items = carrito.get_items()

    if not items:
        messages.warning(request, 'Tu carrito está vacío. Agrega productos antes de comprar.')
        return redirect('catalogo:producto_list')

    total = carrito.get_total()

    if request.method == 'POST':
        # Crear la orden
        orden = Orden.objects.create(usuario=request.user, total=total)

        # Crear los items y descontar stock
        for item in items:
            producto = item['producto']
            cantidad = item['cantidad']

            OrdenItem.objects.create(
                orden=orden,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
            )

            # Descontar stock
            producto.stock -= cantidad
            if producto.stock < 0:
                producto.stock = 0
            producto.save(update_fields=['stock'])

        # Limpiar carrito
        carrito.limpiar()
        messages.success(request, f'Orden #{orden.id} confirmada correctamente.')
        return redirect('ordenes:confirmacion', orden_id=orden.id)

    return render(request, 'ordenes/checkout.html', {'items': items, 'total': total})


@login_required
def confirmacion(request, orden_id):
    """Muestra la confirmación de una orden."""
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)
    return render(request, 'ordenes/confirmacion.html', {'orden': orden})


@login_required
def mis_ordenes(request):
    """Lista las órdenes del usuario autenticado."""
    ordenes = Orden.objects.filter(usuario=request.user)
    return render(request, 'ordenes/mis_ordenes.html', {'ordenes': ordenes})
