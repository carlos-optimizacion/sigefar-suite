from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ArchivoAdjunto, Empresa, LicenciaModulo, ModuloSistema, Notificacion, ParametroGeneral, Producto, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("SIGEFAR", {"fields": ("empresa", "cargo", "telefono")}),)
    list_display = ("username", "email", "first_name", "last_name", "empresa", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("ruc", "razon_social", "nombre_comercial", "pais", "activo")
    search_fields = ("ruc", "razon_social", "nombre_comercial")
    list_filter = ("activo", "pais")


@admin.register(ModuloSistema)
class ModuloSistemaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "obligatorio", "activo")
    search_fields = ("codigo", "nombre")
    list_filter = ("obligatorio", "activo")


@admin.register(LicenciaModulo)
class LicenciaModuloAdmin(admin.ModelAdmin):
    list_display = ("empresa", "modulo", "fecha_inicio", "fecha_fin", "habilitado")
    list_filter = ("habilitado", "modulo")
    search_fields = ("empresa__razon_social", "modulo__codigo")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre_comercial", "principio_activo", "forma_farmaceutica", "estado")
    search_fields = ("codigo", "nombre_comercial", "principio_activo", "titular", "fabricante")
    list_filter = ("estado", "forma_farmaceutica", "pais_origen")


admin.site.register(ArchivoAdjunto)
admin.site.register(ParametroGeneral)
admin.site.register(Notificacion)
