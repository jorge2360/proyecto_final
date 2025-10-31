from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction

from pedidos.models import Pedido, PedidoItem
from pagos.models import Pago
from .models import Carrito, CarritoItem
from productos.models import Producto


# ================================
# Obtener o crear carrito
# ================================
def _get_or_create_cart(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

        session_key = request.session.session_key
        if session_key:
            try:
                session_cart = Carrito.objects.get(
                    session_key=session_key, usuario__isnull=True
                )
                if session_cart != carrito:
                    for s_item in session_cart.items.select_related("producto"):
                        item, _ = CarritoItem.objects.get_or_create(
                            carrito=carrito,
                            producto=s_item.producto,
                            usuario=request.user
                        )
                        item.cantidad += s_item.cantidad
                        item.save()
                    session_cart.delete()
            except Carrito.DoesNotExist:
                pass
        return carrito

    if not request.session.session_key:
        request.session.create()

    carrito, _ = Carrito.objects.get_or_create(
        session_key=request.session.session_key, usuario__isnull=True
    )
    return carrito


# ================================
# Mostrar carrito
# ================================
def detalle_carrito(request):
    carrito = _get_or_create_cart(request)
    items = carrito.items.select_related("producto")
    total = sum(item.producto.precio * item.cantidad for item in items)

    return render(
        request,
        "carrito/detalle.html",
        {"carrito": carrito, "items": items, "total": total},
    )


# ================================
# Agregar producto
# ================================
@require_POST
def agregar_al_carrito(request, producto_id):
    carrito = _get_or_create_cart(request)
    producto = get_object_or_404(Producto, pk=producto_id)

    cantidad = int(request.POST.get("cantidad", 1))
    if cantidad < 1:
        cantidad = 1

    usuario = request.user if request.user.is_authenticated else None

    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": cantidad, "usuario": usuario},
    )

    if not created:
        item.cantidad += cantidad
        item.save()

    messages.success(request, f"“{producto.nombre}” se agregó al carrito.")
    return redirect("carrito:detalle")


# ================================
# Eliminar producto
# ================================
@require_POST
def eliminar_item(request, producto_id):
    carrito = _get_or_create_cart(request)
    try:
        item = CarritoItem.objects.get(carrito=carrito, producto_id=producto_id)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
            messages.info(request, f"Se redujo la cantidad de {item.producto.nombre}.")
        else:
            item.delete()
            messages.info(request, "Producto eliminado del carrito.")
    except CarritoItem.DoesNotExist:
        messages.warning(request, "Ese producto no estaba en tu carrito.")
    return redirect("carrito:detalle")


# ================================
# Vaciar carrito
# ================================
def vaciar_carrito(request):
    carrito = _get_or_create_cart(request)
    carrito.items.all().delete()
    messages.info(request, "Carrito vaciado.")
    return redirect("carrito:detalle")


# ================================
# Checkout (pago)
# ================================
@login_required
@transaction.atomic
def checkout(request):
    carrito = _get_or_create_cart(request)
    items = carrito.items.select_related("producto")

    if not items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("productos:lista")

    total = sum(item.producto.precio * item.cantidad for item in items)

    if request.method == "POST":
        metodo_pago = request.POST.get("metodo_pago")
        if metodo_pago not in ["transferencia", "tarjeta", "efectivo"]:
            messages.error(request, "Seleccione un método de pago válido.")
            return redirect("carrito:checkout")

        try:
            # ✅ Dirección de envío asegurada (nunca NULL)
            direccion_envio = (
                request.POST.get("direccion_envio")
                or getattr(request.user, "direccion", None)
                or "Dirección no especificada"
            )

            # 1️⃣ Crear pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                direccion_envio=direccion_envio,
                total=total,
                estado="pendiente"
            )

            # 2️⃣ Crear ítems y descontar stock
            for item in items:
                producto = item.producto

                if producto.stock < item.cantidad:
                    messages.warning(request, f"Stock insuficiente para {producto.nombre}.")
                    pedido.delete()
                    return redirect("carrito:detalle")

                producto.stock -= item.cantidad
                producto.save()

                PedidoItem.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item.cantidad,
                    precio=producto.precio,
                )

            # 3️⃣ Registrar pago
            Pago.objects.create(
                pedido=pedido,
                usuario=request.user,
                metodo=metodo_pago,
                monto=total,
                confirmado=False,
            )

            # 4️⃣ Vaciar carrito
            carrito.items.all().delete()

            messages.success(request, f"¡Pedido #{pedido.id} creado correctamente!")
            print(f"[CHECKOUT OK] Pedido #{pedido.id} | Usuario: {request.user.username} | Total: {total}")
            return redirect("carrito:confirmacion", pedido_id=pedido.id)

        except Exception as e:
            print(f"[CHECKOUT ERROR] {type(e).__name__}: {e}")
            messages.error(request, "Ocurrió un error al procesar tu compra. Intenta nuevamente.")
            return redirect("carrito:detalle")

    return render(
        request,
        "pagos/checkout.html",
        {"carrito": carrito, "items": items, "total": total}
    )
@login_required
def confirmacion(request, pedido_id):
    """Pantalla de confirmación de compra"""
    from pedidos.models import Pedido  # evitar import circular
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    return render(request, "carrito/confirmacion.html", {"pedido": pedido})
