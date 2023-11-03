import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
django.setup()

from django.contrib.auth.models import User
from faker import Faker
from random import choice
from cms.cmsapp.models import Tarea, Post, Comment, Category

fake = Faker()

# Crea usuarios
for _ in range(10):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    user = User.objects.create_user(username=username, email=email, password=password)

# Crea tareas
for _ in range(20):
    usuario = choice(User.objects.all())
    titulo = fake.text(20)
    descripcion = fake.text(100)
    estado = choice(['pendiente', 'en_proceso', 'completada'])
    eliminada = choice([True, False])
    Tarea.objects.create(usuario=usuario, titulo=titulo, descripcion=descripcion, estado=estado, eliminada=eliminada)

# Crea categorías
categorias = ['Categoria 1', 'Categoria 2', 'Categoria 3']
for categoria in categorias:
    Category.objects.create(title=categoria, slug=slugify(categoria))

# Crea publicaciones
for _ in range(30):
    writer = choice(User.objects.all())
    title = fake.text(50)
    tipo = choice(['Texto', 'Imagenes', 'Combinados', 'Otros'])
    category = choice(Category.objects.all())
    body = fake.text(200)
    post = Post.objects.create(writer=writer, title=title, tipo=tipo, category=category, body=body, slug=slugify(title))

# Crea comentarios
for _ in range(50):
    content = fake.text(200)
    author = choice(User.objects.all())
    post = choice(Post.objects.all())
    Comment.objects.create(content=content, author=author, post=post)

print("Datos insertados exitosamente.")
