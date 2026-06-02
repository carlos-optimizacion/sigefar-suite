from django.db import models

from bpa.models import LoteBPA
from core.models import ModeloBase, Producto, Usuario
from qms.models import Desviacion


class CasoFarmacovigilancia(ModeloBase):
    TIPOS_EVENTO = [
        ("RAM", "Sospecha de RAM"),
        ("EVENTO_ADVERSO", "Evento adverso"),
        ("ERROR_MEDICACION", "Error de medicación"),
        ("FALTA_EFICACIA", "Falta de eficacia"),
        ("PRM", "Problema relacionado con medicamento"),
    ]
    ESTADOS = [("BORRADOR", "Borrador"), ("VALIDACION", "Validación"), ("SEGUIMIENTO", "Seguimiento"), ("CERRADO", "Cerrado")]
    GRAVEDAD = [("NO_GRAVE", "No grave"), ("GRAVE", "Grave"), ("NO_EVALUADA", "No evaluada")]

    codigo = models.CharField(max_length=80, unique=True)
    tipo_evento = models.CharField(max_length=40, choices=TIPOS_EVENTO)
    producto_sospechoso = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="casos_bpfv")
    numero_lote_reportado = models.CharField(max_length=120, blank=True)
    fecha_vencimiento_reportada = models.DateField(null=True, blank=True)
    lote_bpa_vinculado = models.ForeignKey(LoteBPA, on_delete=models.PROTECT, null=True, blank=True, related_name="casos_bpfv")
    lote_no_encontrado_bpa = models.BooleanField(default=False)
    descripcion = models.TextField()
    gravedad = models.CharField(max_length=20, choices=GRAVEDAD, default="NO_EVALUADA")
    causalidad = models.CharField(max_length=120, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="BORRADOR")
    reportado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="casos_bpfv_reportados")
    desviacion_qms = models.ForeignKey(Desviacion, on_delete=models.PROTECT, null=True, blank=True, related_name="casos_bpfv")

    class Meta:
        verbose_name = "Caso de farmacovigilancia"
        verbose_name_plural = "Casos de farmacovigilancia"
        ordering = ["-creado_en"]
        indexes = [models.Index(fields=["codigo"]), models.Index(fields=["numero_lote_reportado"])]

    def __str__(self):
        return f"{self.codigo} - {self.producto_sospechoso}"


class SeguimientoCaso(ModeloBase):
    caso = models.ForeignKey(CasoFarmacovigilancia, on_delete=models.CASCADE, related_name="seguimientos")
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="seguimientos_bpfv")
    archivo = models.FileField(upload_to="bpfv/seguimientos/%Y/%m/", null=True, blank=True)

    class Meta:
        verbose_name = "Seguimiento de caso"
        verbose_name_plural = "Seguimientos de casos"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Seguimiento {self.caso.codigo}"
