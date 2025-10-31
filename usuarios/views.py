from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import ClienteRegistroForm, AdminRegistroForm
from django.contrib.auth.decorators import login_required


# --- Registro cliente ---
def registro_cliente(request):
    if request.method == "POST":
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Cuenta de cliente creada exitosamente. ¡Bienvenido!")
            return redirect("home")
        else:
            messages.error(request, "Hubo un error al registrarse. Verifica los datos.")
    else:
        form = ClienteRegistroForm()
    return render(request, "usuarios/registro.html", {"form": form, "tipo": "cliente"})


# --- Registro administrador ---
def registro_admin(request):
    if request.method == "POST":
        form = AdminRegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Cuenta de administrador creada exitosamente.")
            return redirect("home")
        else:
            messages.error(request, "Error al registrar administrador.")
    else:
        form = AdminRegistroForm()
    return render(request, "usuarios/registro.html", {"form": form, "tipo": "admin"})


# --- Login ---
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f"Bienvenido {usuario.username}")
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})


# --- Logout ---
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("home")
# --- Perfil de usuario ---
@login_required
def perfil(request):
    return render(request, "usuarios/perfil.html")