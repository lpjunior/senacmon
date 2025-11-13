from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction

from game.models import Partida, EventoRodada, Batalha
from wallet.models import Transacao

User = get_user_model()

class Command(BaseCommand):
    help = "Reseta partidas, batalhas, eventos e transações. Pode atuar por usuário ou global."

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            type=str,
            help="Username para resetar dados somente deste usuário"
        )
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Confirma execução destrutiva sem prompt"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username = options.get("user")
        confirm = options.get("confirm")

        if not confirm:
            raise CommandError("Use --confirm para confirmar a operação.")

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f"Usuário '{username}' não encontrado.")
            # apaga em ordem segura
            tx_qs = Transacao.objects.filter(user=user)
            part_qs = Partida.objects.filter(user=user)
            ev_qs = EventoRodada.objects.filter(partida__in=part_qs)
            bat_qs = Batalha.objects.filter(partida__in=part_qs)

            deleted = {
                "transacoes": tx_qs.count(),
                "batalhas": bat_qs.count(),
                "eventos": ev_qs.count(),
                "partidas": part_qs.count(),
            }
            tx_qs.delete()
            bat_qs.delete()
            ev_qs.delete()
            part_qs.delete()

            self.stdout.write(self.style.SUCCESS(
                f"Reset concluído para '{username}': {deleted}"
            ))
        else:
            # global
            deleted = {
                "transacoes": Transacao.objects.count(),
                "batalhas": Batalha.objects.count(),
                "eventos": EventoRodada.objects.count(),
                "partidas": Partida.objects.count(),
            }
            Transacao.objects.all().delete()
            Batalha.objects.all().delete()
            EventoRodada.objects.all().delete()
            Partida.objects.all().delete()

            self.stdout.write(self.style.SUCCESS(
                f"Reset global concluído: {deleted}"
            ))
