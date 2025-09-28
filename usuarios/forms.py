from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'contraseña', 'direccion', 'telefono']
        widgets = {
            'contraseña': forms.PasswordInput(),
        }
