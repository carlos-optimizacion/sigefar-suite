from django.contrib import admin

from .models import EventoAuditoria


@admin.register(EventoAuditoria)
class EventoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "usuario", "accion", "modulo", "entidad", "entidad_id")
    search_fields = ("usuario__username", "modulo", "entidad", "descripcion")
    list_filter = ("accion", "modulo")
    readonly_fields = ("fecha",)
