from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.panel_inicio, name='inicio'),
    path('productos/', views.productos_lista, name='productos_lista'),
    path('productos/nuevo/', views.producto_crear, name='producto_crear'),
    path('productos/editar/<int:pk>/', views.producto_editar, name='producto_editar'),
    path('productos/eliminar/<int:pk>/', views.producto_eliminar, name='producto_eliminar'),
    path('pedidos/', views.pedidos_lista, name='pedidos_lista'),
    path('pedidos/estado/<int:pk>/', views.pedido_cambiar_estado, name='pedido_cambiar_estado'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),

]
