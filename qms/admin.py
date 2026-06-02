from django.contrib import admin

from .models import CAPA, Desviacion, DocumentoControlado, DocumentoRegulatorioProducto, RegistroSanitario


@admin.register(DocumentoControlado)
class DocumentoControladoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "titulo", "version", "estado", "responsable", "fecha_vigencia")
    search_fields = ("codigo", "titulo")
    list_filter = ("estado",)


@admin.register(RegistroSanitario)
class RegistroSanitarioAdmin(admin.ModelAdmin):
    list_display = ("producto", "numero_registro", "titular", "fecha_vencimiento", "activo")
    search_fields = ("numero_registro", "producto__nombre_comercial", "titular")
    list_filter = ("activo",)


@admin.register(DocumentoRegulatorioProducto)
class DocumentoRegulatorioProductoAdmin(admin.ModelAdmin):
    list_display = ("producto", "tipo", "documento_controlado")
    search_fields = ("producto__nombre_comercial", "documento_controlado__codigo")
    list_filter = ("tipo",)


@admin.register(Desviacion)
class DesviacionAdmin(admin.ModelAdmin):
    list_display = ("codigo", "origen", "titulo", "producto", "estado", "reportado_por")
    search_fields = ("codigo", "titulo", "descripcion")
    list_filter = ("origen", "estado")


@admin.register(CAPA)
class CAPAAdmin(admin.ModelAdmin):
    list_display = ("codigo", "responsable", "estado", "fecha_compromiso", "fecha_cierre")
    search_fields = ("codigo", "descripcion")
    list_filter = ("estado",)
