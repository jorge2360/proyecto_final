from django.db import models

class Usuario(models.Model):
    ROLES = [
        ('cliente', 'Cliente'),
        ('admin', 'Admin'),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=10, choices=ROLES, default='cliente')
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
