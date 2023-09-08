"""from django.contrib.auth.models import User, Group
from django.test import TestCase, User
from django.urls import reverse
from permisos.views import *
from permisos.models import RolesdeSistema
#test para las funciones de views.py de roles

class Test_rol_views(TestCase):

    def setUp(self):
        self.user = User()
        self.rol = RolesdeSistema.objects.create(nombre='testRol', descripcion='testRol')

    def test_crearRol(self):
        path = reverse('crear_rol')
        response = self.user.get(path)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permisos/crear_rol.html')

    def test_listarRoles(self):
        path = reverse('listar_roles')
        response = self.user.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permisos/listar_roles.html')

    def test_modificarRol(self):
        path = reverse('modificar_rol', args=[self.rol.id])
        response = self.user.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permisos/modificar_rol.html')

    def test_eliminarRol(self):
        path = reverse('eliminar_rol', args=[self.rol.id])
        response = self.user.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permisos/eliminar_rol.html')
"""