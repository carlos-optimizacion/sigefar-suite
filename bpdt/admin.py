from django.contrib import admin

from .models import IncidenteTransporte, Transportista, VehiculoAutorizado


@admin.register(Transportista)
class TransportistaAdmin(admin.ModelAdmin):
    list_display = ("ruc", "razon_social", "contacto", "telefono", "autorizado", "activo")
    search_fields = ("ruc", "razon_social", "contacto")
    list_filter = ("autorizado", "activo")


@admin.register(VehiculoAutorizado)
class VehiculoAutorizadoAdmin(admin.ModelAdmin):
    list_display = ("placa", "transportista", "tipo", "autorizado", "activo")
    search_fields = ("placa", "transportista__razon_social")
    list_filter = ("autorizado", "activo")


@admin.register(IncidenteTransporte)
class IncidenteTransporteAdmin(admin.ModelAdmin):
    list_display = ("tipo", "transportista", "vehiculo", "producto", "fecha_evento", "reportado_por")
    search_fields = ("descripcion", "transportista__razon_social", "vehiculo__placa")
    list_filter = ("tipo", "transportista")
