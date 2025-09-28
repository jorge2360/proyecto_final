from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    # Página principal de productos destacados
    path("", views.index, name="index"),

    # Lista completa de productos
    path("lista/", views.lista_productos, name="lista"),

    # Detalle de un producto específico
    path("<int:pk>/", views.detalle_producto, name="detalle"),

    # Vista por categoría (ej: /productos/categoria/Hombres/)
    path("categoria/<str:nombre>/", views.productos_por_categoria, name="categoria"),
]
