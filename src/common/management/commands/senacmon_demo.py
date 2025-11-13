from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from game.services.partida_service import start_game, rolar_dados_e_resolver_zona, consume_capture_cooldown
from game.services.batalha_service import resolver_batalha
from game.services.aposta_service import preparar_e_cobrar_aposta, pagar_premio
from game.domain.regras import PoliticaMultiplicador
from game.choices import EstadoPartida

User = get_user_model()

class Command(BaseCommand):
    help = "Cria uma partida demo autojogável para apresentação em aula"

    def add_arguments(self, parser):
        parser.add_argument(
            "--rounds",
            type=int,
            default=5,
            help="Quantidade de rodadas para simulação (default: 5)"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        rounds = options["rounds"]

        # cria/pega usuário
        user, _ = User.objects.get_or_create(
            username="demo",
            defaults={"password": "demo1234"}
        )

        # limpa partidas antigas
        Partida.objects.filter(user=user).delete()

        # prepara entidades base
        starter = Pokemon.objects.filter(ativo=True).first()
        mapa = Mapa.objects.filter(ativo=True).first()

        # cria partida
        partida = start_game(user, starter, mapa)
        self.stdout.write(self.style.SUCCESS(
            f"Partida demo criada com Pokémon inicial: {starter.nome}"
        ))

        policy = PoliticaMultiplicador()

        for _ in range(rounds):
            # caso esteja capturado, apenas avança
            if consume_capture_cooldown(partida):
                self.stdout.write(self.style.WARNING(
                    "[captura] Rodada pulada."
                ))
                continue

            # rola dado e resolve zona
            result = rolar_dados_e_resolver_zona(partida)
            zona = result["zona"]
            rodada = partida.rodada_atual - (0 if zona == "batalha" else 1)

            self.stdout.write(f"[rodada {rodada}] Zona: {zona}")

            # se gerar batalha, resolver automaticamente
            if zona == "batalha":
                batalha = Batalha.objects.get(partida=partida, rodada=rodada)

                # escolha automática
                numeros = [1, 4]  # ex.: dois números fixos
                aposta = 5

                try:
                    preparar_e_cobrar_aposta(user, partida, numeros, aposta, 5, 8, 20)
                    batalha = resolver_batalha(batalha, numeros, aposta, False, policy)
                    if batalha.resultado == "vitoria":
                        pagar_premio(user, partida, batalha.berries_delta)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[batalha] Resultado: {batalha.resultado}, Delta: {batalha.berries_delta}"
                        )
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"[erro batalha] {e}")
                    )

        self.stdout.write(self.style.SUCCESS(
            f"\nPartida demo completa! Acesse com o usuário 'demo' no /game/state/"
        ))
        self.stdout.write(self.style.SUCCESS(
            "Senha padrão: demo1234"
        ))
