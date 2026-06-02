from django.db import models
from django.conf import settings


class EventoAuditoria(models.Model):
    ACCIONES = [("CREATE", "Crear"), ("UPDATE", "Actualizar"), ("DELETE", "Eliminar"), ("LOGIN", "Ingreso"), ("EXPORT", "Exportar")]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    modulo = models.CharField(max_length=40)
    entidad = models.CharField(max_length=120)
    entidad_id = models.CharField(max_length=80, blank=True)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = "Evento de auditoría"
        verbose_name_plural = "Eventos de auditoría"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.fecha} - {self.accion} - {self.entidad}"
