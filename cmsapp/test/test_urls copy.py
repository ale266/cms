
from unittest import TestCase
import pytest
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from userprofile.models import UserProfile
from userprofile.views import signin, account, UpdateProfile, DeleteProfile, signout, registration, profile
from django.contrib.auth.models import User
"""
Haciendo pytest con URLS de userprofile
"""
@pytest.mark.django_db
class Test_urls(TestCase):
  def setUp(self):
    self.user =  User.objects.create(username='test')


  def test_profile(self):
    url = reverse('profile',args=[self.user.id])
    self.assertEqual(resolve(url).func,profile)

  def test_login(self):
    url = reverse('signin')
    self.assertEqual(resolve(url).func,signin)

  def test_logout(self):
    url = reverse('signout')
    self.assertEqual(resolve(url).func,signout)
    
  def test_UpdateProfile(self):
    url = reverse('updateprofile')
    self.assertEqual(resolve(url).func,UpdateProfile)

  def test_DeleteProfile(self):
    url = reverse('deleteprofile')
    self.assertEqual(resolve(url).func,DeleteProfile)

  def test_account(self):
    url = reverse('account')
    self.assertEqual(resolve(url).func,account)

  def test_registration(self):
    url = reverse('registration')
    self.assertEqual(resolve(url).func,registration)

  def test_logout(self):
    url = reverse('signout')
    self.assertEqual(resolve(url).func,signout)