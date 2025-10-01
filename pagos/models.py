from django.db import models
from django.conf import settings

# Ejemplo simple: un pago asociado a un usuario
class Pago(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pago #{self.id} - {self.usuario} - {self.total}"
