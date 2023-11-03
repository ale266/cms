import random
from django.core.management.base import BaseCommand
from cms.cmsapp.models import Tarea, tipoPost, estadoPost, RolUsuario, Carrousel, Post, Comment, Category
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Puebla la base de datos con datos de prueba'

    def handle(self, *args, **options):
        # Crear usuarios
        for _ in range(10):
            User.objects.create(username=f'Usuario{_}')

        # Crear tareas
        for _ in range(10):
            usuario = random.choice(User.objects.all())
            estado = random.choice(['pendiente', 'en_proceso', 'completada'])
            Tarea.objects.create(usuario=usuario, titulo=f'Tarea {_}', descripcion=f'Descripción de la tarea {_}', estado=estado)

        # Crear roles de usuario
        for usuario in User.objects.all():
            roles = RolUsuario.objects.create(miembro=usuario)
            # Asignar roles aleatorios a los usuarios
            # roles.roles.set(random.sample(list(RolesdeSistema.objects.all()), k=random.randint(1, 3)))

        # Crear categorías
        for _ in range(3):
            Category.objects.create(title=f'Categoría {_}', slug=f'categoria{_}')

        # Crear carrouseles
        for _ in range(5):
            Carrousel.objects.create(image=f'carrousel{_}.jpg', description=f'Descripción del carrousel {_}')

        # Crear posts
        for _ in range(10):
            writer = random.choice(User.objects.all())
            tipo = random.choice([tipoPost.TEXTO, tipoPost.IMAGENES, tipoPost.COMBINADOS, tipoPost.OTROS])
            category = random.choice(Category.objects.all())
            estado = random.choice([estadoPost.CREACION, estadoPost.ENEDICION, estadoPost.PUBLICACION, estadoPost.DESACTIVADO])
            post = Post.objects.create(writer=writer, title=f'Título del Post {_}', tipo=tipo, category=category, estado=estado)
            post.carrousel.set(random.sample(list(Carrousel.objects.all()), k=random.randint(0, 3)))

            # Crear comentarios en los posts
            for _ in range(random.randint(0, 5)):
                autor = random.choice(User.objects.all())
                Comment.objects.create(content=f'Comentario {_} en {post.title}', author=autor, post=post)

        self.stdout.write(self.style.SUCCESS('Base de datos poblada con éxito'))
