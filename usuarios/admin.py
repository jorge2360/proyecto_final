from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    # Qué campos mostrar en la lista de usuarios
    list_display = ("username", "email", "rol", "is_staff", "is_superuser")
    list_filter = ("rol", "is_staff", "is_superuser", "is_active")

    # Qué campos se editan dentro de cada usuario
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Información Personal", {"fields": ("telefono", "direccion", "rol")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Campos para cuando se crea un usuario en el admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "telefono", "direccion", "rol", "password1", "password2"),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)

# Registrar el modelo en el admin
admin.site.register(Usuario, UsuarioAdmin)
