# pedidos/views.py
from django.shortcuts import get_object_or_404, render
from .models import Pedido

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items = pedido.items.select_related("producto")
    return render(request, "pedidos/detalle.html", {"pedido": pedido, "items": items})
