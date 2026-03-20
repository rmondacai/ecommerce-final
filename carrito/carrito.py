"""Carrito basado en sesión de Django."""
from catalogo.models import Producto


class Carrito:
    """Maneja el carrito de compras almacenado en la sesión del usuario."""

    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        """Agrega un producto o incrementa su cantidad."""
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'cantidad': 0,
                'precio': producto.precio,
            }
        self.carrito[producto_id]['cantidad'] += cantidad
        self.guardar()

    def quitar(self, producto):
        """Elimina un producto del carrito."""
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def actualizar_cantidad(self, producto, cantidad):
        """Actualiza la cantidad de un producto."""
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            if cantidad > 0:
                self.carrito[producto_id]['cantidad'] = cantidad
            else:
                del self.carrito[producto_id]
            self.guardar()

    def guardar(self):
        self.session.modified = True

    def limpiar(self):
        """Vacía el carrito."""
        del self.session['carrito']
        self.session.modified = True

    def get_items(self):
        """Retorna los items del carrito con objetos Producto."""
        producto_ids = self.carrito.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        items = []
        for producto in productos:
            pid = str(producto.id)
            cantidad = self.carrito[pid]['cantidad']
            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': producto.precio * cantidad,
            })
        return items

    def get_total(self):
        """Retorna el total del carrito."""
        items = self.get_items()
        return sum(item['subtotal'] for item in items)

    def get_total_items(self):
        """Retorna la cantidad total de items."""
        return sum(item['cantidad'] for item in self.carrito.values())

    def __len__(self):
        return self.get_total_items()
