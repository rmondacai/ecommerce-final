from django.db import models
from django.conf import settings
from catalogo.models import Producto


class Orden(models.Model):
    """Orden/pedido asociado a un usuario autenticado."""

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('enviada', 'Enviada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ordenes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='confirmada')
    total = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Orden #{self.id} - {self.usuario.username} - {self.get_estado_display()}'

    def calcular_total(self):
        self.total = sum(item.subtotal for item in self.items.all())
        self.save(update_fields=['total'])


class OrdenItem(models.Model):
    """Línea de detalle de una orden."""
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()

    class Meta:
        verbose_name = 'Ítem de Orden'
        verbose_name_plural = 'Ítems de Orden'

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f'{self.cantidad}x {self.producto.nombre}'
