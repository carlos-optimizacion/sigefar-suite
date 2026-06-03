from django.contrib import admin

from .models import CAPA, Desviacion, DocumentoControlado


@admin.register(DocumentoControlado)
class DocumentoControladoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "titulo", "tipo_sgi", "version", "estado", "responsable", "fecha_vigencia", "activo")
    search_fields = ("codigo", "titulo", "historial_cambios")
    list_filter = ("tipo_sgi", "estado", "activo")
    list_select_related = ("responsable",)
    readonly_fields = ("creado_en", "actualizado_en")
    fieldsets = (
        ("Documento del Sistema de Gestión Integrado", {"fields": ("codigo", "titulo", "tipo_sgi", "version", "estado")}),
        ("Control documental SGI", {"fields": ("responsable", "fecha_emision", "fecha_vigencia", "archivo", "historial_cambios")}),
        ("Control", {"fields": ("activo", "creado_en", "actualizado_en")}),
    )


@admin.register(Desviacion)
class DesviacionAdmin(admin.ModelAdmin):
    list_display = ("codigo", "origen", "titulo", "producto_regulatorio", "estado", "reportado_por", "activo")
    search_fields = ("codigo", "titulo", "descripcion", "producto_regulatorio__codigo", "producto_regulatorio__nombre_comercial")
    list_filter = ("origen", "estado", "activo")
    list_select_related = ("producto_regulatorio", "reportado_por")
    readonly_fields = ("creado_en", "actualizado_en")


@admin.register(CAPA)
class CAPAAdmin(admin.ModelAdmin):
    list_display = ("codigo", "responsable", "estado", "fecha_compromiso", "fecha_cierre", "activo")
    search_fields = ("codigo", "descripcion", "verificacion_eficacia")
    list_filter = ("estado", "activo")
    list_select_related = ("responsable", "desviacion")
    readonly_fields = ("creado_en", "actualizado_en")
