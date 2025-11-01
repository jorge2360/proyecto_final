from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from productos.models import Producto
from productos.forms import ProductoForm
from pedidos.models import Pedido
from django.db.models import Sum, Count
import datetime

# Verifica si el usuario es admin o superusuario
def es_admin_tienda(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Administrador de Tienda').exists())

# Dashboard principal
@user_passes_test(es_admin_tienda)
def panel_inicio(request):
    total_productos = Producto.objects.count()
    return render(request, 'dashboard/panel_inicio.html', {
        'total_productos': total_productos
    })

# CRUD Productos
@user_passes_test(es_admin_tienda)
def productos_lista(request):
    productos = Producto.objects.all()
    return render(request, 'dashboard/productos_lista.html', {'productos': productos})

@user_passes_test(es_admin_tienda)
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:productos_lista')
    else:
        form = ProductoForm()
    return render(request, 'dashboard/producto_form.html', {'form': form, 'accion': 'Nuevo'})

@user_passes_test(es_admin_tienda)
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('dashboard:productos_lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'dashboard/producto_form.html', {'form': form, 'accion': 'Editar'})

@user_passes_test(es_admin_tienda)
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('dashboard:productos_lista')

# === LISTA DE PEDIDOS ===
@user_passes_test(es_admin_tienda)
def pedidos_lista(request):
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    return render(request, 'dashboard/pedidos_lista.html', {'pedidos': pedidos})

# === CAMBIO DE ESTADO (opcional rápido) ===
@user_passes_test(es_admin_tienda)
def pedido_cambiar_estado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
        return redirect('dashboard:pedidos_lista')
    return render(request, 'dashboard/pedido_estado_form.html', {'pedido': pedido})

# === ESTADÍSTICAS ===
@user_passes_test(es_admin_tienda)
def estadisticas(request):
    hoy = datetime.date.today()
    total_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.filter(estado='Pendiente').count()
    ventas_totales = Pedido.objects.aggregate(total=Sum('total'))['total'] or 0

    # Gráfico simple: pedidos por mes
    pedidos_por_mes = (
        Pedido.objects
        .extra(select={'mes': "strftime('%%m', fecha_creacion)"})
        .values('mes')
        .annotate(cantidad=Count('id'))
        .order_by('mes')
    )

    context = {
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'ventas_totales': ventas_totales,
        'pedidos_por_mes': pedidos_por_mes,
    }
    return render(request, 'dashboard/estadisticas.html', context)