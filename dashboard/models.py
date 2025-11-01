from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_admin_group(sender, **kwargs):
    if sender.name == 'usuarios':  # evita que se repita
        admin_group, created = Group.objects.get_or_create(name='Administrador de Tienda')
        perms = Permission.objects.filter(content_type__app_label__in=['productos', 'pedidos'])
        admin_group.permissions.set(perms)
