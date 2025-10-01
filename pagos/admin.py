from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "total", "fecha")
    search_fields = ("usuario__username",)
    list_filter = ("fecha",)
