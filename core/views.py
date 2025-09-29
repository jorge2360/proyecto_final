from django.shortcuts import render
from productos.models import Categoria

def home(request):
    categorias = Categoria.objects.all()
    return render(request, "index.html", {"categorias": categorias})
