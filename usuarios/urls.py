from django.urls import path
from . import views
from .views import CustomLoginView

app_name = "usuarios"

urlpatterns = [
    path("registro/", views.registro_cliente, name="registro_cliente"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("perfil/", views.perfil, name="perfil"),
]
