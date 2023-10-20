import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from cmsapp.models import *

from cmsapp.views import *



"""
test para los urls del Proyecto
"""
class Test_proyecto_urls(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='testProyecto')
        self.miembro = User.objects.create( username='testMiembro')

    def test_crearPost(self):
        url = reverse('create')
        self.assertEqual(resolve(url).func, createPost, "no se pudo crear proyecto")

    def test_asignar_miembro(self):
        url = reverse('asignar_miembro', args=[self.post.slug])
        self.assertEqual(resolve(url).func, asignarMiembro)

    def test_asignarRol(self):
        url = reverse('asignar_rol', args=[self.post.slug, self.miembro.id])
        self.assertEqual(resolve(url).func, asignarRol)
