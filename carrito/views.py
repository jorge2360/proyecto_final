from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Carrito, CarritoItem
from productos.models import Producto


def _get_or_create_cart(request):
    """
    Obtiene o crea el carrito para el usuario actual.
    - Si está autenticado, usa su carrito personal.
    - Si es anónimo, usa el session_key.
    - Fusiona carrito de sesión con el de usuario al iniciar sesión.
    """
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
# Mostrar el carrito
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
# Agregar producto al carrito
# ================================
@require_POST
def agregar_al_carrito(request, producto_id):
    carrito = _get_or_create_cart(request)
    producto = get_object_or_404(Producto, pk=producto_id)

    try:
        cantidad = int(request.POST.get("cantidad", 1))
        if cantidad < 1:
            cantidad = 1
    except (TypeError, ValueError):
        cantidad = 1

    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": cantidad, "usuario": getattr(request.user, "id", None)},
    )

    if not created:
        item.cantidad += cantidad
        item.save()

    messages.success(request, f"“{producto.nombre}” se agregó al carrito.")
    return redirect("carrito:detalle")


# ================================
# Eliminar un ítem
# ================================
def eliminar_item(request, producto_id):
    carrito = _get_or_create_cart(request)
    try:
        item = CarritoItem.objects.get(carrito=carrito, producto_id=producto_id)
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
def checkout(request):
    carrito = _get_or_create_cart(request)
    items = carrito.items.select_related("producto")
    total = sum(item.producto.precio * item.cantidad for item in items)

    if not items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("productos:lista")

    return render(request, "pagos/checkout.html", {"carrito": carrito, "items": items, "total": total})
