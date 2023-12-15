import django
from django.test import TestCase
# Create your tests here.
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings.development')

django.setup()
import pytest
from cmsapp.models import Category

def test_example():
    assert 1 == 1


def test_example2():
    assert 1 == 1
def test_example3():
    assert 1 == 1
def test_example4():
    assert 1 == 1
def test_example5():
    assert 1 == 1
def test_example6():
    assert 1 == 1

    
@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(title="Social")
    assert category.title == "Social"