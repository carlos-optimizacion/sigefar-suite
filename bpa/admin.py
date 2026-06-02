from django.contrib import admin

from .models import AlmacenRegulado, ExcursionBPA, LoteBPA, ZonaRegulada


@admin.register(AlmacenRegulado)
class AlmacenReguladoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "responsable", "activo")
    search_fields = ("codigo", "nombre", "direccion")
    list_filter = ("activo",)


@admin.register(ZonaRegulada)
class ZonaReguladaAdmin(admin.ModelAdmin):
    list_display = ("almacen", "codigo", "nombre", "tipo", "activo")
    search_fields = ("codigo", "nombre", "almacen__nombre")
    list_filter = ("tipo", "activo")


@admin.register(LoteBPA)
class LoteBPAAdmin(admin.ModelAdmin):
    list_display = ("producto", "numero_lote", "fecha_vencimiento", "estado_regulatorio", "almacen", "zona")
    search_fields = ("numero_lote", "producto__codigo", "producto__nombre_comercial")
    list_filter = ("estado_regulatorio", "almacen")


@admin.register(ExcursionBPA)
class ExcursionBPAAdmin(admin.ModelAdmin):
    list_display = ("almacen", "lote", "fecha_inicio", "fecha_fin", "temperatura_min", "temperatura_max")
    search_fields = ("descripcion", "lote__numero_lote")
    list_filter = ("almacen",)
