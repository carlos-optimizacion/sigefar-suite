from django.contrib import admin

from .models import (
    DocumentoRegulatorioProducto,
    ExpedienteDIGEMID,
    ObservacionAutoridad,
    ProductoRegulatorio,
    RegistroSanitarioRegulatorio,
    SubsanacionRegulatoria,
)


class RegulatorioAdminBase(admin.ModelAdmin):
    readonly_fields = ("creado_en", "actualizado_en")
    list_per_page = 25

    def activar(self, request, queryset):
        queryset.update(activo=True)

    activar.short_description = "Activar registros seleccionados"

    def inactivar(self, request, queryset):
        queryset.update(activo=False)

    inactivar.short_description = "Inactivar registros seleccionados"


@admin.register(ProductoRegulatorio)
class ProductoRegulatorioAdmin(RegulatorioAdminBase):
    list_display = ("codigo", "nombre_comercial", "categoria", "estado_regulatorio", "titular", "fabricante", "responsable_regulatorio", "activo")
    search_fields = ("codigo", "nombre_comercial", "principio_activo", "titular", "fabricante")
    list_filter = ("categoria", "estado_regulatorio", "activo", "pais_origen")
    list_select_related = ("empresa", "responsable_regulatorio")
    ordering = ("nombre_comercial", "codigo")
    actions = ("activar", "inactivar")
    fieldsets = (
        ("Identificación regulatoria", {"fields": ("empresa", "codigo", "nombre_comercial", "categoria", "estado_regulatorio")}),
        ("Características aprobadas", {"fields": ("principio_activo", "forma_farmaceutica", "concentracion", "presentacion")}),
        ("Titularidad y fabricación", {"fields": ("titular", "fabricante", "pais_origen")}),
        ("Condiciones aprobadas", {"fields": ("condiciones_almacenamiento", "condiciones_transporte")}),
        ("Responsabilidad y control", {"fields": ("responsable_regulatorio", "activo", "creado_en", "actualizado_en")}),
    )


@admin.register(ExpedienteDIGEMID)
class ExpedienteDIGEMIDAdmin(RegulatorioAdminBase):
    list_display = ("numero_expediente", "producto", "tipo", "estado", "fecha_presentacion", "fecha_resolucion", "responsable", "activo")
    search_fields = ("numero_expediente", "producto__codigo", "producto__nombre_comercial", "comentario")
    list_filter = ("tipo", "estado", "activo")
    list_select_related = ("producto", "responsable")
    ordering = ("-creado_en",)
    actions = ("activar", "inactivar")


@admin.register(RegistroSanitarioRegulatorio)
class RegistroSanitarioRegulatorioAdmin(RegulatorioAdminBase):
    list_display = ("numero_registro", "producto", "estado", "fecha_emision", "fecha_vencimiento", "activo")
    search_fields = ("numero_registro", "producto__codigo", "producto__nombre_comercial")
    list_filter = ("estado", "activo", "fecha_vencimiento")
    list_select_related = ("producto", "expediente_origen")
    ordering = ("fecha_vencimiento", "producto__nombre_comercial")
    actions = ("activar", "inactivar")


@admin.register(DocumentoRegulatorioProducto)
class DocumentoRegulatorioProductoAdmin(RegulatorioAdminBase):
    list_display = ("producto", "tipo", "codigo_documento", "titulo", "version", "fecha_aprobacion", "activo")
    search_fields = ("producto__codigo", "producto__nombre_comercial", "codigo_documento", "titulo")
    list_filter = ("tipo", "activo", "fecha_aprobacion")
    list_select_related = ("producto", "expediente")
    ordering = ("producto__nombre_comercial", "tipo", "-fecha_aprobacion")
    actions = ("activar", "inactivar")


@admin.register(ObservacionAutoridad)
class ObservacionAutoridadAdmin(RegulatorioAdminBase):
    list_display = ("expediente", "fecha_observacion", "fecha_limite_respuesta", "respondida", "activo")
    search_fields = ("expediente__numero_expediente", "descripcion")
    list_filter = ("respondida", "activo", "fecha_limite_respuesta")
    list_select_related = ("expediente",)
    ordering = ("-fecha_observacion",)
    actions = ("activar", "inactivar")


@admin.register(SubsanacionRegulatoria)
class SubsanacionRegulatoriaAdmin(RegulatorioAdminBase):
    list_display = ("observacion", "fecha_respuesta", "presentado_por", "activo")
    search_fields = ("observacion__expediente__numero_expediente", "descripcion")
    list_filter = ("activo", "fecha_respuesta")
    list_select_related = ("observacion", "presentado_por")
    ordering = ("-fecha_respuesta",)
    actions = ("activar", "inactivar")
