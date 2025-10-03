from decimal import Decimal
from django.conf import settings
from django.db import models
from productos.models import Producto


class Carrito(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="carritos",
    )
    session_key = models.CharField(
        max_length=40, null=True, blank=True, db_index=True
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Carrito de {self.user}"
        return f"Carrito sesión {self.session_key}"

    @property
    def total(self):
        total = Decimal("0.00")
        for item in self.items.select_related("producto"):
            total += item.subtotal
        return total


class CarritoItem(models.Model):
    carrito = models.ForeignKey(
        Carrito, on_delete=models.CASCADE, related_name="items"
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("carrito", "producto")

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

    @property
    def subtotal(self):
        if self.producto and self.producto.precio is not None:
            return self.producto.precio * self.cantidad
        return Decimal("0.00")
