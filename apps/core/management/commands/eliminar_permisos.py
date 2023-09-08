# Importa los modelos necesarios
import os
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")

# Configura Django
settings.configure()
import django

django.setup()
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Define la función para eliminar permisos
def eliminar_permisos():
    # Encuentra el modelo o la aplicación para la que deseas eliminar permisos
    content_type = ContentType.objects.get(app_label='permisos', model='RolesdeSistema')

    # Lista de nombres de permisos que deseas eliminar
    permisos_a_eliminar = [
        ('_acceder_al_sistema','Acceder al sistema'),
        ('_crear_usuario', 'Crear usuario'),
        ('_crear_proyecto', 'Crear Proyecto'),
        ('_crear_sprint', 'Crear sprint'),
        ('_crear_us','Crear US'),
    ]

    # Itera sobre los nombres de permisos y elimínalos
    for nombre_permiso in permisos_a_eliminar:
        try:
            permiso = Permission.objects.get(codename=nombre_permiso, content_type=content_type)
            permiso.delete()
            print(f"Permiso {nombre_permiso} eliminado correctamente.")
        except Permission.DoesNotExist:
            print(f"El permiso {nombre_permiso} no existe.")

if __name__ == '__main__':
    eliminar_permisos()