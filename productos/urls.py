from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    path("lista/", views.lista_productos, name="lista"),
    path("<int:pk>/", views.detalle_producto, name="detalle"),
    path("categoria/<str:nombre>/", views.productos_por_categoria, name="categoria"),
]
