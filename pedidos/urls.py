from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path("<int:pedido_id>/", views.detalle_pedido, name="detalle"),
    path('lista/', views.lista_pedidos, name='lista'), 
]
