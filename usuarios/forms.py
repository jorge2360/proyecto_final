from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class ClienteRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["username", "email", "telefono", "direccion", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = "cliente"   # importante: se asigna automáticamente
        if commit:
            user.save()
        return user


class AdminRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["username", "email", "telefono", "direccion", "rol", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # lo forzamos como administrador
        if commit:
            user.save()
        return user
