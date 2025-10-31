from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class ClienteRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["username", "email", "telefono", "direccion", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese su nombre de usuario"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "ejemplo@correo.com"
            }),
            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Número de teléfono"
            }),
            "direccion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Dirección de entrega"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizamos los campos de contraseña
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Cree una contraseña segura"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirme su contraseña"
        })
        # Mensajes más claros
        self.fields["password1"].help_text = "Use al menos 8 caracteres, incluyendo letras y números."
        self.fields["password2"].help_text = "Repita la contraseña para confirmarla."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = "cliente"
        if commit:
            user.save()
        return user


class AdminRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["username", "email", "telefono", "direccion", "rol", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre de usuario"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Correo electrónico"
            }),
            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Teléfono"
            }),
            "direccion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Dirección completa"
            }),
            "rol": forms.Select(attrs={
                "class": "form-select"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Contraseña"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirmar contraseña"
        })
        self.fields["password1"].help_text = "Debe tener al menos 8 caracteres."
        self.fields["password2"].help_text = "Repita la contraseña para confirmar."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user
