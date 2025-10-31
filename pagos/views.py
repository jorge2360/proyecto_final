from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from carrito.models import Carrito
from pedidos.models import Pedido, PedidoItem


@login_required
def checkout(request):
    """
    Vista de confirmación de compra.
    Muestra resumen del carrito y permite registrar el pedido.
    """
    # Obtiene el carrito del usuario logueado
    try:
        carrito = Carrito.objects.get(usuario=request.user)
    except Carrito.DoesNotExist:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("productos:lista")

    items = carrito.items.select_related("producto")
    total = sum(item.producto.precio * item.cantidad for item in items)

    # Procesar formulario POST (confirmar pedido)
    if request.method == "POST":
        direccion = request.POST.get("direccion_envio")

        if not direccion:
            messages.error(request, "Debe ingresar una dirección de envío.")
            return redirect("pagos:checkout")

        # Crear el pedido
        pedido = Pedido.objects.create(
            usuario=request.user,
            direccion_envio=getattr(request.user, "direccion", "Sin dirección registrada"),
            total=total,
            estado="pendiente"
        )

        # Crear los items del pedido
        for item in items:
            PedidoItem.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.producto.precio,
            )

        # Vaciar carrito
        carrito.items.all().delete()

        messages.success(request, "Su pedido fue realizado con éxito.")
        return redirect("pedidos:detalle", pedido_id=pedido.id)

    return render(request, "pagos/checkout.html", {"items": items, "total": total})
