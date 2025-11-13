from django.core.management.base import BaseCommand
from django.db import transaction
from game.models import Pokemon
from game.choices import Elemento

# sprites livres, substitua por seus assets locais quando desejar
SPRITES = {
    "Bulbasaur": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
    "Ivysaur": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png",
    "Charmander": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
    "Charmeleon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png",
    "Squirtle": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png",
    "Wartortle": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/8.png",
    "Chikorita": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/152.png",
    "Cyndaquil": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/155.png",
    "Totodile": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/158.png",
}

EXTRAS = [
    # planta
    dict(nome="Ivysaur", elemento=Elemento.PLANTA, numero_associado=2),
    dict(nome="Chikorita", elemento=Elemento.PLANTA, numero_associado=3),
    # fogo
    dict(nome="Charmeleon", elemento=Elemento.FOGO, numero_associado=5),
    dict(nome="Cyndaquil", elemento=Elemento.FOGO, numero_associado=8),
    # água
    dict(nome="Wartortle", elemento=Elemento.AGUA, numero_associado=9),
    dict(nome="Totodile", elemento=Elemento.AGUA, numero_associado=0),
]

STARTERS_FIX = [
    # reforça starters com sprite caso seed inicial não tenha
    dict(nome="Bulbasaur", elemento=Elemento.PLANTA, numero_associado=6),
    dict(nome="Charmander", elemento=Elemento.FOGO, numero_associado=4),
    dict(nome="Squirtle", elemento=Elemento.AGUA, numero_associado=1),
]

class Command(BaseCommand):
    help = "Adiciona pokémons extras, atribui sprite_url e garante elementos água, fogo e planta."

    @transaction.atomic
    def handle(self, *args, **options):
        created, updated = 0, 0

        # starters com sprite
        for p in STARTERS_FIX:
            obj, was_created = Pokemon.objects.update_or_create(
                nome=p["nome"],
                defaults=dict(
                    elemento=p["elemento"],
                    numero_associado=p["numero_associado"],
                    ativo=True,
                    sprite_url=SPRITES.get(p["nome"], ""),
                ),
            )
            created += int(was_created)
            updated += int(not was_created)

        # extras
        for p in EXTRAS:
            obj, was_created = Pokemon.objects.update_or_create(
                nome=p["nome"],
                defaults=dict(
                    elemento=p["elemento"],
                    numero_associado=p["numero_associado"],
                    ativo=True,
                    sprite_url=SPRITES.get(p["nome"], ""),
                ),
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"Extras aplicados. Criados {created}, Atualizados {updated}"
        ))
