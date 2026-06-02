from django.db import models

from core.models import ModeloBase, Producto, Usuario
from qms.models import Desviacion


class Transportista(ModeloBase):
    ruc = models.CharField(max_length=20, unique=True)
    razon_social = models.CharField(max_length=200)
    contacto = models.CharField(max_length=160, blank=True)
    telefono = models.CharField(max_length=40, blank=True)
    autorizado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Transportista"
        verbose_name_plural = "Transportistas"
        ordering = ["razon_social"]

    def __str__(self):
        return self.razon_social


class VehiculoAutorizado(ModeloBase):
    transportista = models.ForeignKey(Transportista, on_delete=models.PROTECT, related_name="vehiculos")
    placa = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=120, blank=True)
    capacidad_referencial = models.CharField(max_length=120, blank=True)
    autorizado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vehículo autorizado"
        verbose_name_plural = "Vehículos autorizados"
        ordering = ["placa"]

    def __str__(self):
        return self.placa


class IncidenteTransporte(ModeloBase):
    TIPOS = [("EXCURSION", "Excursión"), ("INCIDENTE", "Incidente"), ("DEVOLUCION", "Devolución"), ("ENTREGA_FALLIDA", "Entrega fallida")]
    transportista = models.ForeignKey(Transportista, on_delete=models.PROTECT, related_name="incidentes")
    vehiculo = models.ForeignKey(VehiculoAutorizado, on_delete=models.PROTECT, null=True, blank=True, related_name="incidentes")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)
    tipo = models.CharField(max_length=30, choices=TIPOS)
    descripcion = models.TextField()
    fecha_evento = models.DateTimeField()
    reportado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="incidentes_bpdt")
    desviacion_qms = models.ForeignKey(Desviacion, on_delete=models.PROTECT, null=True, blank=True, related_name="incidentes_bpdt")

    class Meta:
        verbose_name = "Incidente BPDT"
        verbose_name_plural = "Incidentes BPDT"
        ordering = ["-fecha_evento"]

    def __str__(self):
        return f"{self.tipo} - {self.fecha_evento}"
