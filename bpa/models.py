from django.db import models

from core.models import ModeloBase, Producto, Usuario
from qms.models import Desviacion


class AlmacenRegulado(ModeloBase):
    codigo = models.CharField(max_length=60, unique=True)
    nombre = models.CharField(max_length=180)
    direccion = models.CharField(max_length=255, blank=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="almacenes_bpa")

    class Meta:
        verbose_name = "Almacén regulado"
        verbose_name_plural = "Almacenes regulados"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class ZonaRegulada(ModeloBase):
    TIPOS = [("CUARENTENA", "Cuarentena"), ("APROBADO", "Aprobado"), ("RECHAZADO", "Rechazado"), ("DEVOLUCION", "Devolución"), ("OTRA", "Otra")]
    almacen = models.ForeignKey(AlmacenRegulado, on_delete=models.PROTECT, related_name="zonas")
    codigo = models.CharField(max_length=60)
    nombre = models.CharField(max_length=180)
    tipo = models.CharField(max_length=30, choices=TIPOS)

    class Meta:
        verbose_name = "Zona regulada"
        verbose_name_plural = "Zonas reguladas"
        unique_together = [("almacen", "codigo")]

    def __str__(self):
        return f"{self.almacen.codigo} - {self.codigo}"


class LoteBPA(ModeloBase):
    ESTADOS = [
        ("CUARENTENA", "Cuarentena"),
        ("LIBERADO", "Liberado"),
        ("OBSERVADO", "Observado"),
        ("BLOQUEADO", "Bloqueado"),
        ("RECHAZADO", "Rechazado"),
        ("DEVUELTO", "Devuelto"),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="lotes_bpa")
    numero_lote = models.CharField(max_length=120)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado_regulatorio = models.CharField(max_length=30, choices=ESTADOS, default="CUARENTENA")
    almacen = models.ForeignKey(AlmacenRegulado, on_delete=models.PROTECT, null=True, blank=True)
    zona = models.ForeignKey(ZonaRegulada, on_delete=models.PROTECT, null=True, blank=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="lotes_bpa_registrados")
    motivo_estado = models.TextField(blank=True)
    evidencia = models.FileField(upload_to="bpa/lotes/%Y/%m/", null=True, blank=True)

    class Meta:
        verbose_name = "Lote BPA"
        verbose_name_plural = "Lotes BPA"
        ordering = ["producto", "numero_lote"]
        indexes = [models.Index(fields=["numero_lote"]), models.Index(fields=["producto", "numero_lote"])]

    def __str__(self):
        return f"{self.producto.codigo} - {self.numero_lote}"


class ExcursionBPA(ModeloBase):
    lote = models.ForeignKey(LoteBPA, on_delete=models.PROTECT, related_name="excursiones", null=True, blank=True)
    almacen = models.ForeignKey(AlmacenRegulado, on_delete=models.PROTECT, related_name="excursiones")
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    temperatura_min = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    temperatura_max = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    descripcion = models.TextField()
    desviacion_qms = models.ForeignKey(Desviacion, on_delete=models.PROTECT, null=True, blank=True, related_name="excursiones_bpa")

    class Meta:
        verbose_name = "Excursión BPA"
        verbose_name_plural = "Excursiones BPA"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"Excursión BPA {self.fecha_inicio}"
