# pedidos/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Pedido

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-creado')
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})

@login_required
def detalle_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
    return render(request, 'pedidos/detalle.html', {'pedido': pedido})
