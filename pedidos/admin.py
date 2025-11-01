from django.contrib import admin
from .models import Pedido, PedidoItem


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio', 'subtotal_display')

    def subtotal_display(self, obj):
        return f"Q{obj.subtotal():.2f}"
    subtotal_display.short_description = "Subtotal"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mostrar_cliente', 'mostrar_fecha', 'estado', 'mostrar_total')
    list_filter = ('estado', 'creado')
    search_fields = ('usuario__username', 'usuario__email')
    ordering = ('-creado',)
    readonly_fields = ('creado', 'actualizado', 'total')
    inlines = [PedidoItemInline]

    # ✅ Muestra el nombre del cliente (o username si no tiene nombre completo)
    def mostrar_cliente(self, obj):
        if obj.usuario.first_name or obj.usuario.last_name:
            return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip()
        return obj.usuario.username
    mostrar_cliente.short_description = "Cliente"

    # ✅ Muestra la fecha con formato legible
    def mostrar_fecha(self, obj):
        return obj.creado.strftime("%d/%m/%Y %H:%M")
    mostrar_fecha.short_description = "Fecha"

    # ✅ Muestra el total con símbolo Q
    def mostrar_total(self, obj):
        return f"Q{obj.total:.2f}"
    mostrar_total.short_description = "Total"


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio', 'subtotal_display')

    def subtotal_display(self, obj):
        return f"Q{obj.subtotal():.2f}"
    subtotal_display.short_description = "Subtotal"
