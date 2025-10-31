from django.contrib import admin
from .models import Carrito, CarritoItem


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "session_key", "creado", "actualizado")
    search_fields = ("usuario__username", "session_key")


@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ("id", "carrito", "producto", "cantidad", "usuario", "creado", "actualizado")
    search_fields = ("producto__nombre", "usuario__username")
    list_select_related = ("carrito", "producto", "usuario")
