from .carrito import Carrito


def carrito_total_items(request):
    """Inyecta el total de items del carrito en todos los templates."""
    carrito = Carrito(request)
    return {'carrito_total_items': len(carrito)}
