from django.db import models
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, default='')
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default='')
    precio = models.IntegerField(validators=[MinValueValidator(1, message='El precio debe ser mayor a $0.')])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0, message='El stock no puede ser negativo.')])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen_url = models.URLField(blank=True, default='')
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre
