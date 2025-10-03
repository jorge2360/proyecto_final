from django.contrib import admin
from .models import Carrito, CarritoItem


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "creado", "actualizado")
    search_fields = ("user__username", "session_key")


@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ("id", "carrito", "producto", "cantidad", "creado", "actualizado")
    search_fields = ("producto__nombre",)
    list_select_related = ("carrito", "producto")
