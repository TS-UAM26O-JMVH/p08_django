#codigo 11. permite automatizar la creacion de un superusuario para pruebas, 
# evitando la creacion manual de usuarios y facilitando la validacion de autenticacion mediante JWT
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Crea un superusuario inicial para pruebas JWT"

    def handle(self, *args, **kwargs):

        username = "Admin"
        email = "admin@tecnologias.com"
        password = "AdmApiDjango123"

        # Verificar si ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"El usuario '{username}' ya existe."
                )
            )
            return

        # Crear superusuario
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Superusuario '{username}' creado correctamente."
            )
        )