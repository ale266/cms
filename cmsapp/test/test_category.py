import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from cmsapp.models import Category
from cmsapp.views import *
from permisos.views import modificar_rol, listar_roles, crear_rol, eliminar_rol
from permisos.models import *

"""
test para los urls de los roles del sistema
"""
class Test_urls(TestCase):

  def setUp(self):
    self.category = Category.objects.create(title='testCat')


  def test_crearCat(self):
    url = reverse('createCategory')
    self.assertEqual(resolve(url).func, createCategory, "no se pudo dirigir a el url home")

  def test_eliminarCat(self):
    url = reverse('deleteCategory', args=[self.category.category_id])
    self.assertEqual(resolve(url).func, deleteCategory)

  
  def test_modificarCat(self):
    url = reverse('updateCategory', args=[self.category.category_id])
    self.assertEqual(resolve(url).func, updateCategory)
   

  
@pytest.mark.django_db
def test_mi_vista_lista(client):
    url = reverse('listCategory')

    # Realiza una solicitud GET a la URL
    response = client.get(url)

    # Verifica que la respuesta sea exitosa (código 200)
    assert response.status_code == 200