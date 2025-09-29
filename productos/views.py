from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

# Página de inicio - mostrar categorías
def home(request):
    categorias = Categoria.objects.all()
    return render(request, "index.html", {"categorias": categorias})

# Listado de productos
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos/lista.html", {"productos": productos})

# Detalle de producto
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "productos/detalle.html", {"producto": producto})

# Productos por categoría
def productos_por_categoria(request, nombre):
    categoria = get_object_or_404(Categoria, nombre__iexact=nombre)  # sin distinguir mayúsculas
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, "productos/categoria.html", {
        "categoria": categoria,
        "productos": productos,
    })
