from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from .models import Producto


# Página de inicio - categorías y destacados
def home(request):
    categorias = Categoria.objects.all()

    # productos destacados por categoria usando ID 
    destacados_mujeres = Producto.objects.filter(categoria_id=6, destacado=True)[:8]
    destacados_hombres = Producto.objects.filter(categoria_id=5, destacado=True)[:8]
    destacados_ninos = Producto.objects.filter(categoria_id=7, destacado=True)[:8]
    destacados_accesorios = Producto.objects.filter(categoria_id=8, destacado=True)[:8]

    return render(request, "index.html", {
        "categorias": categorias,
        "destacados_mujeres": destacados_mujeres,
        "destacados_hombres": destacados_hombres,
        "destacados_ninos": destacados_ninos,
        "destacados_accesorios": destacados_accesorios,
    })


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
    categoria = get_object_or_404(Categoria, nombre__iexact=nombre)  
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, "productos/categoria.html", {
        "categoria": categoria,
        "productos": productos,
    })

def buscar_producto(request):
    query = request.GET.get("q")
    resultados = Producto.objects.filter(nombre__icontains=query) if query else []
    return render(request, "productos/buscar.html", {"resultados": resultados, "query": query})

def buscar_ajax(request):
    q = request.GET.get("q", "").strip()
    results = []
    if q:
        qs = (Producto.objects
              .filter(nombre__icontains=q)[:10]
              .values("id", "nombre", "precio", "imagen"))
        for p in qs:
            results.append({
                "id": p["id"],
                "nombre": p["nombre"],
                "precio": str(p["precio"]),
                "imagen": getattr(getattr(Producto.objects.get(id=p["id"]), "imagen"), "url", ""),
                "url": reverse("productos:detalle", args=[p["id"]]),
            })
    return JsonResponse({"results": results})