from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Carrito, CarritoItem
from productos.models import Producto


def _get_or_create_cart(request):
    """
    Obtiene el carrito para el usuario autenticado o crea/recupera uno por sesión
    para usuarios anónimos. También fusiona carrito de sesión al loguearse.
    """
    # Usuario autenticado
    if request.user.is_authenticated:
        cart, _ = Carrito.objects.get_or_create(user=request.user)

        # Si existe carrito de sesión, fusionarlo
        if request.session.session_key:
            try:
                session_cart = Carrito.objects.get(
                    session_key=request.session.session_key, user__isnull=True
                )
                if session_cart != cart:
                    for s_item in session_cart.items.select_related("producto"):
                        item, _ = CarritoItem.objects.get_or_create(
                            carrito=cart, producto=s_item.producto
                        )
                        item.cantidad += s_item.cantidad
                        item.save()
                    session_cart.delete()
            except Carrito.DoesNotExist:
                pass

        return cart

    # Usuario anónimo (por sesión)
    if not request.session.session_key:
        request.session.create()
    cart, _ = Carrito.objects.get_or_create(
        session_key=request.session.session_key, user__isnull=True
    )
    return cart


def detalle_carrito(request):
    carrito = _get_or_create_cart(request)
    # Prefetch para eficiencia
    items = carrito.items.select_related("producto")
    return render(request, "carrito/detalle.html", {"carrito": carrito, "items": items})


@require_POST
def agregar_al_carrito(request, producto_id):
    carrito = _get_or_create_cart(request)
    producto = get_object_or_404(Producto, pk=producto_id)

    # cantidad por POST (default=1)
    try:
        cantidad = int(request.POST.get("cantidad", "1"))
        if cantidad < 1:
            cantidad = 1
    except (TypeError, ValueError):
        cantidad = 1

    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito, producto=producto
    )
    if created:
        item.cantidad = cantidad
    else:
        item.cantidad += cantidad
    item.save()

    messages.success(request, f"“{producto.nombre}” se agregó al carrito.")
    return redirect("carrito:detalle")


def eliminar_item(request, producto_id):
    carrito = _get_or_create_cart(request)
    try:
        item = CarritoItem.objects.get(carrito=carrito, producto_id=producto_id)
        item.delete()
        messages.info(request, "Producto eliminado del carrito.")
    except CarritoItem.DoesNotExist:
        messages.warning(request, "Ese producto no estaba en tu carrito.")
    return redirect("carrito:detalle")


def vaciar_carrito(request):
    carrito = _get_or_create_cart(request)
    carrito.items.all().delete()
    messages.info(request, "Carrito vaciado.")
    return redirect("carrito:detalle")
