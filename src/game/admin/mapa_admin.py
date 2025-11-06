from django.contrib import admin, messages
from django.db import transaction
from ..models.mapa import Mapa, MapaPosicao
from ..choices import TipoZona

class MapaPosicaoInline(admin.TabularInline):
    model = MapaPosicao
    extra = 0
    fields = ("posicao", "tipo_zona", "valor_param")
    ordering = ("posicao",)
    min_num = 0
    verbose_name = "Posição do mapa"
    verbose_name_plural = "Posições do mapa"

@admin.register(Mapa)
class MapaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "tamanho_total", "ativo", "config_hash")
    list_filter = ("ativo",)
    search_fields = ("nome", "config_hash")
    ordering = ("-id",)
    inlines = [MapaPosicaoInline]
    actions = ["ativar", "desativar", "duplicar_mapa"]

    @admin.action(description="Ativar mapas selecionados")
    def ativar(self, request, queryset):
        updated = queryset.update(ativo=True)
        self.message_user(request, f"{updated} mapa(s) ativado(s).", level=messages.SUCCESS)

    @admin.action(description="Desativar mapas selecionados")
    def desativar(self, request, queryset):
        updated = queryset.update(ativo=False)
        self.message_user(request, f"{updated} mapa(s) desativado(s).", level=messages.WARNING)

    @admin.action(description="Duplicar mapas selecionados")
    def duplicar_mapa(self, request, queryset):
        count = 0
        with transaction.atomic():
            for mapa in queryset:
                novo = Mapa.objects.create(
                    nome=f"{mapa.nome} (cópia)",
                    tamanho_total=mapa.tamanho_total,
                    ativo=False,
                    config_hash=mapa.config_hash or "",
                )
                posicoes = [
                    MapaPosicao(
                        mapa=novo,
                        posicao=mp.posicao,
                        tipo_zona=mp.tipo_zona,
                        valor_param=mp.valor_param,
                    )
                    for mp in MapaPosicao.objects.filter(mapa=mapa).order_by("posicao")
                ]
                MapaPosicao.objects.bulk_create(posicoes)
                count += 1
        self.message_user(request, f"{count} mapa(s) duplicado(s).", level=messages.SUCCESS)

@admin.register(MapaPosicao)
class MapaPosicaoAdmin(admin.ModelAdmin):
    list_display = ("id", "mapa", "posicao", "tipo_zona", "valor_param")
    list_filter = ("tipo_zona", "mapa__ativo")
    search_fields = ("mapa__nome",)
    ordering = ("mapa", "posicao")
    autocomplete_fields = ("mapa",)
    readonly_fields = ()
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("mapa")
