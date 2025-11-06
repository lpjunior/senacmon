from django.core.management.base import BaseCommand
from django.db import transaction

from game.choices import Elemento, TipoZona
from game.models import Pokemon, Mapa, MapaPosicao


class Command(BaseCommand):
    help = "Carrega seeds iniciais do Senacmon"

    @transaction.atomic
    def handle(self, *args, **options):
        # starters
        starters = [
            dict(nome="Bulbasaur", elemento=Elemento.PLANTA, numero_associado=6),
            dict(nome="Charmander", elemento=Elemento.FOGO, numero_associado=4),
            dict(nome="Squirtle", elemento=Elemento.AGUA, numero_associado=1),
        ]
        for s in starters:
            Pokemon.objects.update_or_create(
                nome=s["nome"],
                defaults=dict(elemento=s["elemento"], numero_associado=s["numero_associado"], ativo=True)
            )

        # mapa simples de 30 posições
        mapa, _ = Mapa.objects.get_or_create(
            nome="Mapa MVP",
            defaults=dict(tamanho_total=30, ativo=True)
        )
        if not mapa.posicoes.exists():
            # distribuição de zonas sugerida
            zonas = ["batalha"] * 8 + ["captura"] * 2 + ["bonus"] * 6 + ["perda"] * 6
            # completa com zona neutra
            while len(zonas) < mapa.tamanho_total:
                zonas.append("neutra")

            for i, z in enumerate(zonas, start=1):
                val = 10 if z == "bonus" else (-5 if z == "perda" else None)
                MapaPosicao.objects.create(
                    mapa=mapa,
                    posicao=i,
                    tipo_zona=getattr(TipoZona, z.upper()),
                    valor_param=val,
                )
            # Resultado 8 batalhas, 2 capturas, 6 bônus, 6 perdas, 8 neutras
        self.stdout.write(self.style.SUCCESS("Seeds aplicadas com sucesso!"))