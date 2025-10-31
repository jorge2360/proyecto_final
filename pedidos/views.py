from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from carrito.models import CarritoItem
from .models import Pedido, DetallePedido
from django.contrib import messages

@login_required
def checkout(request):
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    if not carrito_items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("carrito:detalle")

    total = sum(item.subtotal() for item in carrito_items)

    if request.method == "POST":
        pedido = Pedido.objects.create(usuario=request.user, total=total, estado="pendiente")

        for item in carrito_items:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                subtotal=item.subtotal()
            )
            item.producto.stock -= item.cantidad
            item.producto.save()

        carrito_items.delete()  # limpiar carrito
        messages.success(request, f"Pedido #{pedido.id} realizado con éxito.")
        return redirect("home")

    return render(request, "pedidos/checkout.html", {"items": carrito_items, "total": total})
