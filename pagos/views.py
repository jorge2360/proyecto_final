from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Página inicial de pagos (placeholder)
def index(request):
    return render(request, "pagos/index.html")

# Checkout (requiere login)
@login_required
def checkout(request):
    return render(request, "pagos/checkout.html")
