from django.db import models
from django.conf import settings
from pedidos.models import Pedido

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pagos")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=20, choices=[
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ])
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    confirmado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago #{self.id} - Pedido #{self.pedido.id} - {self.usuario.username}"
