from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from estoque.models import User

class Command(BaseCommand):
    help = "Cria usuários admin iniciais"

    def handle(self, *args, **options):
        admin = [
            {
                "name": "Augusto",
                "jobTitle": "Administrador",
                "email": "augustoinacio243@gmail.com",
                "role": User.Role.ADMIN,
                "password": make_password(";w<33B?T8_RS?")
            },
        ]

        for item in admin:
            if not User.objects.filter(email=item["email"]).exists():
                User.objects.create(**item)
                self.stdout.write(self.style.SUCCESS(f'Usuário {item["email"]} criado com sucesso'))
            else:
                self.stdout.write(self.style.WARNING(f'Usuário {item["email"]} já existe'))