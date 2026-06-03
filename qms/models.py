from django.db import models

from core.models import ModeloBase, Usuario
from regulatorio.models import ProductoRegulatorio


class DocumentoControlado(ModeloBase):
    ESTADOS = [
        ("BORRADOR", "Borrador"),
        ("REVISION", "En revisión"),
        ("APROBADO", "Aprobado"),
        ("VIGENTE", "Vigente"),
        ("OBSOLETO", "Obsoleto"),
    ]
    TIPOS_SGI = [
        ("MANUAL", "Manual"),
        ("PROCEDIMIENTO", "Procedimiento"),
        ("INSTRUCTIVO", "Instructivo"),
        ("FORMATO", "Formato"),
        ("REGISTRO_INTERNO", "Registro interno"),
        ("PROGRAMA", "Programa"),
        ("PLAN", "Plan"),
        ("MATRIZ", "Matriz"),
        ("POLITICA", "Política"),
        ("OTRO_SGI", "Otro documento SGI"),
    ]

    codigo = models.CharField(max_length=80, unique=True)
    titulo = models.CharField(max_length=255)
    tipo_sgi = models.CharField(max_length=40, choices=TIPOS_SGI, default="PROCEDIMIENTO")
    version = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="BORRADOR")
    responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="documentos_responsable")
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vigencia = models.DateField(null=True, blank=True)
    archivo = models.FileField(upload_to="qms/documentos_sgi/%Y/%m/", null=True, blank=True)
    historial_cambios = models.TextField(blank=True)

    class Meta:
        verbose_name = "Documento del SGI"
        verbose_name_plural = "Documentos del SGI"
        ordering = ["codigo", "version"]

    def __str__(self):
        return f"{self.codigo} v{self.version} - {self.titulo}"


class Desviacion(ModeloBase):
    ORIGENES = [("QMS", "Calidad"), ("REG", "Regulatorio"), ("BPA", "BPA"), ("BPDT", "BPDT"), ("BPFV", "BPFV")]
    ESTADOS = [("ABIERTA", "Abierta"), ("INVESTIGACION", "En investigación"), ("CERRADA", "Cerrada")]
    codigo = models.CharField(max_length=80, unique=True)
    origen = models.CharField(max_length=20, choices=ORIGENES)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    producto_regulatorio = models.ForeignKey(ProductoRegulatorio, on_delete=models.PROTECT, null=True, blank=True, related_name="desviaciones_qms")
    reportado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="desviaciones_reportadas")
    estado = models.CharField(max_length=20, choices=ESTADOS, default="ABIERTA")

    class Meta:
        verbose_name = "Desviación"
        verbose_name_plural = "Desviaciones"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"


class CAPA(ModeloBase):
    ESTADOS = [("ABIERTA", "Abierta"), ("EN_PROCESO", "En proceso"), ("VERIFICACION", "Verificación de eficacia"), ("CERRADA", "Cerrada")]
    codigo = models.CharField(max_length=80, unique=True)
    desviacion = models.ForeignKey(Desviacion, on_delete=models.PROTECT, related_name="capas", null=True, blank=True)
    descripcion = models.TextField()
    responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="capas_responsable")
    fecha_compromiso = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="ABIERTA")
    verificacion_eficacia = models.TextField(blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "CAPA"
        verbose_name_plural = "CAPA"
        ordering = ["-creado_en"]

    def __str__(self):
        return self.codigo
