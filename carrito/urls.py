from django.urls import path
from . import views

app_name = "carrito"

urlpatterns = [
    path("", views.detalle_carrito, name="detalle"),
    path("agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar"),
    path("eliminar/<int:producto_id>/", views.eliminar_item, name="eliminar"),
    path("vaciar/", views.vaciar_carrito, name="vaciar"),
    path("checkout/", views.checkout, name="checkout"),
]
