from django.contrib import admin
from .models import Orden, OrdenItem


class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    readonly_fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal')
    extra = 0

    def subtotal(self, obj):
        return f"${obj.subtotal:,.0f}".replace(",", ".")


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'total', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    readonly_fields = ('usuario', 'total', 'fecha_creacion')
    inlines = [OrdenItemInline]
