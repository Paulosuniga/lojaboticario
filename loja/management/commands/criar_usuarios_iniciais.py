import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Cria usuarios iniciais (superuser) a partir da variavel de ambiente "
        "BOOTSTRAP_SUPERUSERS, no formato 'usuario1:senha1,usuario2:senha2'. "
        "Nao faz nada se o usuario ja existir ou a variavel nao estiver definida."
    )

    def handle(self, *args, **options):
        raw = os.environ.get("BOOTSTRAP_SUPERUSERS", "")
        if not raw:
            return

        for par in raw.split(","):
            par = par.strip()
            if not par or ":" not in par:
                continue
            username, password = par.split(":", 1)
            username = username.strip()
            password = password.strip()
            if not username or not password:
                continue

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"Usuario '{username}' ja existe, pulando.")
                continue

            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f"Usuario '{username}' criado."))
