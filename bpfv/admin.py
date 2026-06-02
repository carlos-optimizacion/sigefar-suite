from django.contrib import admin

from .models import CasoFarmacovigilancia, SeguimientoCaso


@admin.register(CasoFarmacovigilancia)
class CasoFarmacovigilanciaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "tipo_evento", "producto_sospechoso", "numero_lote_reportado", "lote_bpa_vinculado", "gravedad", "estado")
    search_fields = ("codigo", "numero_lote_reportado", "descripcion", "producto_sospechoso__nombre_comercial")
    list_filter = ("tipo_evento", "gravedad", "estado", "lote_no_encontrado_bpa")


@admin.register(SeguimientoCaso)
class SeguimientoCasoAdmin(admin.ModelAdmin):
    list_display = ("caso", "fecha", "responsable", "activo")
    search_fields = ("caso__codigo", "descripcion")
    list_filter = ("activo",)
