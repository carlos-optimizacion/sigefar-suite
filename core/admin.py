from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    ArchivoAdjunto,
    AsignacionRolUsuario,
    BitacoraAccion,
    Cargo,
    Empresa,
    LicenciaModulo,
    ModuloSistema,
    Notificacion,
    ParametroGeneral,
    Producto,
    RolFuncional,
    SedeEmpresa,
    Usuario,
)


class CoreAdminBase(admin.ModelAdmin):
    readonly_fields = ("creado_en", "actualizado_en")
    list_per_page = 25

    def activar(self, request, queryset):
        queryset.update(activo=True)

    activar.short_description = "Activar registros seleccionados"

    def inactivar(self, request, queryset):
        queryset.update(activo=False)

    inactivar.short_description = "Inactivar registros seleccionados"


class SedeEmpresaInline(admin.TabularInline):
    model = SedeEmpresa
    extra = 0
    fields = ("codigo", "nombre", "tipo_sede", "ciudad", "responsable_contacto", "activo")
    show_change_link = True

    class Media:
        css = {"all": ("core/css/admin_empresa_core.css", "core/css/admin_empresa_select_fix.css")}


class AsignacionRolInline(admin.TabularInline):
    model = AsignacionRolUsuario
    fk_name = "usuario"
    extra = 0
    fields = ("rol", "fecha_inicio", "fecha_fin", "activo")


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("SIGEFAR Core", {"fields": ("empresa", "cargo", "cargo_funcional", "telefono")}),)
    list_display = ("username", "email", "first_name", "last_name", "empresa", "cargo_funcional", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "empresa__razon_social", "cargo_funcional__nombre")
    list_filter = ("is_active", "is_staff", "is_superuser", "empresa", "cargo_funcional")
    list_select_related = ("empresa", "cargo_funcional")
    inlines = (AsignacionRolInline,)


@admin.register(Cargo)
class CargoAdmin(CoreAdminBase):
    list_display = ("nombre", "nivel", "activo")
    search_fields = ("nombre", "descripcion", "nivel")
    list_filter = ("nivel", "activo")
    actions = ("activar", "inactivar")


@admin.register(Empresa)
class EmpresaAdmin(CoreAdminBase):
    list_display = ("ruc", "razon_social", "tipo_empresa", "estado_operativo", "tipo_instalacion", "responsable_sistema", "activo")
    search_fields = ("ruc", "razon_social", "nombre_comercial", "representante_legal", "responsable_sistema", "email_contacto")
    list_filter = ("tipo_empresa", "estado_operativo", "tipo_instalacion", "activo", "pais")
    actions = ("activar", "inactivar")
    inlines = (SedeEmpresaInline,)
    fieldsets = (
        ("Identificación", {"fields": ("ruc", "razon_social", "nombre_comercial", "tipo_empresa", "representante_legal")}),
        ("Ubicación y contacto", {"fields": ("direccion", "ciudad", "pais", "email_contacto", "telefono_contacto", "responsable_sistema")}),
        ("Instalación SIGEFAR", {"fields": ("tipo_instalacion", "dominio_sistema", "estado_operativo")}),
        ("Control", {"fields": ("observaciones", "activo", "creado_en", "actualizado_en")}),
    )

    class Media:
        css = {"all": ("core/css/admin_empresa_core.css", "core/css/admin_empresa_select_fix.css")}


@admin.register(SedeEmpresa)
class SedeEmpresaAdmin(CoreAdminBase):
    list_display = ("empresa", "codigo", "nombre", "tipo_sede", "ciudad", "responsable_contacto", "activo")
    search_fields = ("empresa__razon_social", "empresa__ruc", "codigo", "nombre", "responsable_contacto", "email_contacto")
    list_filter = ("tipo_sede", "activo", "pais")
    list_select_related = ("empresa",)
    actions = ("activar", "inactivar")
    fieldsets = (
        ("Empresa y sede", {"fields": ("empresa", "codigo", "nombre", "tipo_sede")}),
        ("Ubicación", {"fields": ("direccion", "ciudad", "pais")}),
        ("Contacto", {"fields": ("responsable_contacto", "email_contacto", "telefono_contacto")}),
        ("Control", {"fields": ("observaciones", "activo", "creado_en", "actualizado_en")}),
    )

    class Media:
        css = {"all": ("core/css/admin_empresa_core.css", "core/css/admin_empresa_select_fix.css")}


@admin.register(ModuloSistema)
class ModuloSistemaAdmin(CoreAdminBase):
    list_display = ("codigo", "nombre", "obligatorio", "activo")
    search_fields = ("codigo", "nombre", "descripcion")
    list_filter = ("obligatorio", "activo")
    actions = ("activar", "inactivar")


@admin.register(RolFuncional)
class RolFuncionalAdmin(CoreAdminBase):
    list_display = ("modulo", "nombre", "nivel", "puede_ver", "puede_crear", "puede_editar", "puede_aprobar", "puede_cerrar", "puede_exportar", "activo")
    search_fields = ("nombre", "descripcion", "modulo__codigo", "modulo__nombre")
    list_filter = ("modulo", "nivel", "activo", "puede_ver", "puede_crear", "puede_editar", "puede_aprobar", "puede_cerrar", "puede_exportar")
    list_select_related = ("modulo",)
    actions = ("activar", "inactivar")


@admin.register(AsignacionRolUsuario)
class AsignacionRolUsuarioAdmin(CoreAdminBase):
    list_display = ("usuario", "rol", "fecha_inicio", "fecha_fin", "activo")
    search_fields = ("usuario__username", "usuario__email", "rol__nombre", "rol__modulo__codigo")
    list_filter = ("rol__modulo", "rol__nivel", "activo")
    list_select_related = ("usuario", "rol", "rol__modulo", "asignado_por")
    actions = ("activar", "inactivar")


@admin.register(LicenciaModulo)
class LicenciaModuloAdmin(CoreAdminBase):
    list_display = ("empresa", "modulo", "fecha_inicio", "fecha_fin", "habilitado", "activo")
    search_fields = ("empresa__razon_social", "empresa__ruc", "modulo__codigo", "modulo__nombre", "clave_local")
    list_filter = ("habilitado", "activo", "modulo")
    list_select_related = ("empresa", "modulo")
    actions = ("activar", "inactivar")


@admin.register(Producto)
class ProductoAdmin(CoreAdminBase):
    list_display = ("codigo", "nombre_comercial", "principio_activo", "forma_farmaceutica", "titular", "estado", "activo")
    search_fields = ("codigo", "nombre_comercial", "principio_activo", "titular", "fabricante")
    list_filter = ("estado", "activo", "forma_farmaceutica", "pais_origen")
    actions = ("activar", "inactivar")


@admin.register(ArchivoAdjunto)
class ArchivoAdjuntoAdmin(CoreAdminBase):
    list_display = ("descripcion", "modulo_origen", "subido_por", "activo", "creado_en")
    search_fields = ("descripcion", "modulo_origen", "subido_por__username")
    list_filter = ("modulo_origen", "activo")
    list_select_related = ("subido_por",)
    actions = ("activar", "inactivar")


@admin.register(ParametroGeneral)
class ParametroGeneralAdmin(CoreAdminBase):
    list_display = ("clave", "descripcion", "activo", "actualizado_en")
    search_fields = ("clave", "valor", "descripcion")
    list_filter = ("activo",)
    actions = ("activar", "inactivar")


@admin.register(Notificacion)
class NotificacionAdmin(CoreAdminBase):
    list_display = ("titulo", "usuario", "leida", "fecha_lectura", "activo", "creado_en")
    search_fields = ("titulo", "mensaje", "usuario__username", "usuario__email")
    list_filter = ("leida", "activo", "creado_en")
    list_select_related = ("usuario",)
    actions = ("activar", "inactivar")


@admin.register(BitacoraAccion)
class BitacoraAccionAdmin(admin.ModelAdmin):
    list_display = ("creado_en", "usuario", "modulo", "accion", "modelo", "objeto_id", "activo")
    search_fields = ("usuario__username", "modulo", "accion", "modelo", "objeto_id", "resumen")
    list_filter = ("modulo", "accion", "activo", "creado_en")
    list_select_related = ("usuario",)
    readonly_fields = ("creado_en", "actualizado_en")
    ordering = ("-creado_en",)
