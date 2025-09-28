from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

def index(request):
    # Productos destacados por categoría
    productos_hombres = Producto.objects.filter(categoria__nombre="Hombres", destacado=True)[:8]
    productos_mujeres = Producto.objects.filter(categoria__nombre="Mujeres", destacado=True)[:8]
    productos_ninos = Producto.objects.filter(categoria__nombre="Niños", destacado=True)[:8]

    return render(request, "productos/index.html", {
        "productos_hombres": productos_hombres,
        "productos_mujeres": productos_mujeres,
        "productos_ninos": productos_ninos,
    })

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos/lista.html", {"productos": productos})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "productos/detalle.html", {"producto": producto})

def productos_por_categoria(request, nombre):
    categoria = get_object_or_404(Categoria, nombre=nombre)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, "productos/categoria.html", {
        "categoria": categoria,
        "productos": productos,
    })
