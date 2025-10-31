from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "metodo", "monto", "confirmado", "creado")
    list_filter = ("metodo", "confirmado", "creado")
    search_fields = ("usuario__username", "metodo")
    list_per_page = 20
