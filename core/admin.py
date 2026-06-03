from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ArchivoAdjunto, Empresa, LicenciaModulo, ModuloSistema, Notificacion, ParametroGeneral, Producto, Usuario


class CoreAdminBase(admin.ModelAdmin):
    readonly_fields = ("creado_en", "actualizado_en")
    list_per_page = 25

    def activar(self, request, queryset):
        queryset.update(activo=True)

    activar.short_description = "Activar registros seleccionados"

    def inactivar(self, request, queryset):
        queryset.update(activo=False)

    inactivar.short_description = "Inactivar registros seleccionados"


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("SIGEFAR Core", {"fields": ("empresa", "cargo", "telefono")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "empresa", "cargo", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "empresa__razon_social")
    list_filter = ("is_active", "is_staff", "is_superuser", "empresa")
    list_select_related = ("empresa",)


@admin.register(Empresa)
class EmpresaAdmin(CoreAdminBase):
    list_display = ("ruc", "razon_social", "nombre_comercial", "pais", "activo", "creado_en")
    search_fields = ("ruc", "razon_social", "nombre_comercial")
    list_filter = ("activo", "pais")
    ordering = ("razon_social",)
    actions = ("activar", "inactivar")
    fieldsets = (
        ("Identificación", {"fields": ("ruc", "razon_social", "nombre_comercial")}),
        ("Ubicación", {"fields": ("direccion", "pais")}),
        ("Control", {"fields": ("activo", "creado_en", "actualizado_en")}),
    )


@admin.register(ModuloSistema)
class ModuloSistemaAdmin(CoreAdminBase):
    list_display = ("codigo", "nombre", "obligatorio", "activo")
    search_fields = ("codigo", "nombre", "descripcion")
    list_filter = ("obligatorio", "activo")
    ordering = ("codigo",)
    actions = ("activar", "inactivar")
    fieldsets = (
        ("Módulo", {"fields": ("codigo", "nombre", "descripcion")}),
        ("Gobierno", {"fields": ("obligatorio", "activo", "creado_en", "actualizado_en")}),
    )


@admin.register(LicenciaModulo)
class LicenciaModuloAdmin(CoreAdminBase):
    list_display = ("empresa", "modulo", "fecha_inicio", "fecha_fin", "habilitado", "activo")
    list_filter = ("habilitado", "activo", "modulo")
    search_fields = ("empresa__razon_social", "empresa__ruc", "modulo__codigo", "modulo__nombre")
    list_select_related = ("empresa", "modulo")
    ordering = ("empresa__razon_social", "modulo__codigo")
    actions = ("activar", "inactivar")
    fieldsets = (
        ("Licencia", {"fields": ("empresa", "modulo", "habilitado")}),
        ("Vigencia", {"fields": ("fecha_inicio", "fecha_fin")}),
        ("Control", {"fields": ("activo", "creado_en", "actualizado_en")}),
    )


@admin.register(Producto)
class ProductoAdmin(CoreAdminBase):
    list_display = ("codigo", "nombre_comercial", "principio_activo", "forma_farmaceutica", "concentracion", "titular", "estado", "activo")
    search_fields = ("codigo", "nombre_comercial", "principio_activo", "titular", "fabricante", "pais_origen")
    list_filter = ("estado", "activo", "forma_farmaceutica", "pais_origen")
    ordering = ("nombre_comercial", "codigo")
    actions = ("activar", "inactivar")
    readonly_fields = CoreAdminBase.readonly_fields
    fieldsets = (
        ("LEGADO TRANSITORIO", {"description": "Producto de Core se conserva temporalmente por compatibilidad. El producto regulatorio oficial se crea y gobierna en SIGEFAR-Regulatorio.", "fields": ("codigo", "nombre_comercial", "estado")}),
        ("Datos heredados", {"fields": ("principio_activo", "forma_farmaceutica", "concentracion", "presentacion", "titular", "fabricante", "pais_origen")}),
        ("Control", {"fields": ("activo", "creado_en", "actualizado_en")}),
    )


@admin.register(ArchivoAdjunto)
class ArchivoAdjuntoAdmin(CoreAdminBase):
    list_display = ("descripcion", "modulo_origen", "subido_por", "activo", "creado_en")
    search_fields = ("descripcion", "modulo_origen", "subido_por__username")
    list_filter = ("modulo_origen", "activo")
    list_select_related = ("subido_por",)
    ordering = ("-creado_en",)
    actions = ("activar", "inactivar")
    fieldsets = (
        ("Adjunto", {"fields": ("modulo_origen", "descripcion", "archivo", "subido_por")}),
        ("Control", {"fields": ("activo", "creado_en", "actualizado_en")}),
    )


@admin.register(ParametroGeneral)
class ParametroGeneralAdmin(CoreAdminBase):
    list_display = ("clave", "descripcion", "activo", "actualizado_en")
    search_fields = ("clave", "valor", "descripcion")
    list_filter = ("activo",)
    ordering = ("clave",)
    actions = ("activar", "inactivar")
    fieldsets = (
        ("Parámetro", {"fields": ("clave", "valor", "descripcion")}),
        ("Control", {"fields": ("activo", "creado_en", "actualizado_en")}),
    )


@admin.register(Notificacion)
class NotificacionAdmin(CoreAdminBase):
    list_display = ("titulo", "usuario", "leida", "fecha_lectura", "activo", "creado_en")
    search_fields = ("titulo", "mensaje", "usuario__username", "usuario__email")
    list_filter = ("leida", "activo", "creado_en")
    list_select_related = ("usuario",)
    ordering = ("-creado_en",)
    actions = ("activar", "inactivar")
    fieldsets = (
        ("Notificación", {"fields": ("usuario", "titulo", "mensaje")}),
        ("Lectura", {"fields": ("leida", "fecha_lectura")}),
        ("Control", {"fields": ("activo", "creado_en", "actualizado_en")}),
    )
