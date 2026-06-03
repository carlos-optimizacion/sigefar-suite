from django.db import models

from core.models import Empresa, ModeloBase, Usuario


class ProductoRegulatorio(ModeloBase):
    ESTADOS = [
        ("EN_EVALUACION", "En evaluación"),
        ("INSCRITO", "Inscrito"),
        ("VIGENTE", "Vigente"),
        ("SUSPENDIDO", "Suspendido"),
        ("CANCELADO", "Cancelado"),
        ("NO_VIGENTE", "No vigente"),
    ]
    CATEGORIAS = [
        ("MEDICAMENTO", "Medicamento"),
        ("DISPOSITIVO", "Dispositivo médico"),
        ("COSMETICO", "Cosmético"),
        ("OTRO", "Otro regulado"),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True, blank=True, related_name="productos_regulatorios")
    codigo = models.CharField(max_length=60, unique=True)
    nombre_comercial = models.CharField(max_length=200)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS, default="MEDICAMENTO")
    principio_activo = models.CharField(max_length=255, blank=True)
    forma_farmaceutica = models.CharField(max_length=120, blank=True)
    concentracion = models.CharField(max_length=120, blank=True)
    presentacion = models.CharField(max_length=200, blank=True)
    titular = models.CharField(max_length=200, blank=True)
    fabricante = models.CharField(max_length=200, blank=True)
    pais_origen = models.CharField(max_length=100, blank=True)
    condiciones_almacenamiento = models.TextField(blank=True)
    condiciones_transporte = models.TextField(blank=True)
    estado_regulatorio = models.CharField(max_length=30, choices=ESTADOS, default="EN_EVALUACION")
    responsable_regulatorio = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name="productos_regulatorios_responsable")

    class Meta:
        verbose_name = "Producto regulatorio"
        verbose_name_plural = "Productos regulatorios"
        ordering = ["nombre_comercial", "codigo"]
        indexes = [models.Index(fields=["codigo"]), models.Index(fields=["nombre_comercial"]), models.Index(fields=["estado_regulatorio"])]

    def __str__(self):
        return f"{self.codigo} - {self.nombre_comercial}"


class ExpedienteDIGEMID(ModeloBase):
    ESTADOS = [
        ("PREPARACION", "Preparación"),
        ("PRESENTADO", "Presentado"),
        ("EVALUACION", "En evaluación"),
        ("OBSERVADO", "Observado"),
        ("SUBSANADO", "Subsanado"),
        ("APROBADO", "Aprobado"),
        ("DENEGADO", "Denegado"),
        ("CERRADO", "Cerrado"),
    ]
    TIPOS = [
        ("INSCRIPCION", "Inscripción"),
        ("RENOVACION", "Renovación"),
        ("REINSCRIPCION", "Reinscripción"),
        ("MODIFICACION", "Modificación post-registro"),
        ("ACTUALIZACION", "Actualización"),
        ("OTRO", "Otro trámite"),
    ]

    producto = models.ForeignKey(ProductoRegulatorio, on_delete=models.PROTECT, related_name="expedientes")
    numero_expediente = models.CharField(max_length=120, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPOS)
    estado = models.CharField(max_length=30, choices=ESTADOS, default="PREPARACION")
    fecha_presentacion = models.DateField(null=True, blank=True)
    fecha_resolucion = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name="expedientes_regulatorios")
    comentario = models.TextField(blank=True)

    class Meta:
        verbose_name = "Expediente DIGEMID"
        verbose_name_plural = "Expedientes DIGEMID"
        ordering = ["-creado_en"]
        indexes = [models.Index(fields=["numero_expediente"]), models.Index(fields=["estado"])]

    def __str__(self):
        return f"{self.numero_expediente} - {self.producto}"


class RegistroSanitarioRegulatorio(ModeloBase):
    ESTADOS = [("VIGENTE", "Vigente"), ("POR_VENCER", "Por vencer"), ("VENCIDO", "Vencido"), ("SUSPENDIDO", "Suspendido"), ("CANCELADO", "Cancelado")]

    producto = models.ForeignKey(ProductoRegulatorio, on_delete=models.PROTECT, related_name="registros_sanitarios")
    numero_registro = models.CharField(max_length=120, unique=True)
    expediente_origen = models.ForeignKey(ExpedienteDIGEMID, on_delete=models.PROTECT, null=True, blank=True, related_name="registros_generados")
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default="VIGENTE")
    resolucion = models.FileField(upload_to="regulatorio/resoluciones/%Y/%m/", null=True, blank=True)

    class Meta:
        verbose_name = "Registro sanitario regulatorio"
        verbose_name_plural = "Registros sanitarios regulatorios"
        ordering = ["producto", "numero_registro"]
        indexes = [models.Index(fields=["numero_registro"]), models.Index(fields=["fecha_vencimiento"])]

    def __str__(self):
        return f"{self.producto} - {self.numero_registro}"


class DocumentoRegulatorioProducto(ModeloBase):
    TIPOS = [
        ("FICHA_TECNICA", "Ficha técnica aprobada"),
        ("INSERTO", "Inserto aprobado"),
        ("ROTULADO_MEDIATO", "Rotulado mediato"),
        ("ROTULADO_INMEDIATO", "Rotulado inmediato"),
        ("CONDICION_ALMACENAMIENTO", "Condición aprobada de almacenamiento"),
        ("CONDICION_TRANSPORTE", "Condición aprobada de transporte"),
        ("CERTIFICADO", "Certificado regulatorio"),
        ("COMUNICACION_AUTORIDAD", "Comunicación de autoridad"),
        ("SUSTENTO", "Documento de sustento"),
    ]

    producto = models.ForeignKey(ProductoRegulatorio, on_delete=models.PROTECT, related_name="documentos_regulatorios")
    expediente = models.ForeignKey(ExpedienteDIGEMID, on_delete=models.PROTECT, null=True, blank=True, related_name="documentos")
    tipo = models.CharField(max_length=40, choices=TIPOS)
    codigo_documento = models.CharField(max_length=80, blank=True)
    titulo = models.CharField(max_length=255)
    version = models.CharField(max_length=30, blank=True)
    fecha_aprobacion = models.DateField(null=True, blank=True)
    archivo = models.FileField(upload_to="regulatorio/documentos/%Y/%m/", null=True, blank=True)
    observacion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Documento regulatorio del producto"
        verbose_name_plural = "Documentos regulatorios del producto"
        ordering = ["producto", "tipo", "-fecha_aprobacion"]
        indexes = [models.Index(fields=["tipo"]), models.Index(fields=["codigo_documento"])]

    def __str__(self):
        return f"{self.producto} - {self.get_tipo_display()}"


class ObservacionAutoridad(ModeloBase):
    expediente = models.ForeignKey(ExpedienteDIGEMID, on_delete=models.PROTECT, related_name="observaciones")
    fecha_observacion = models.DateField()
    descripcion = models.TextField()
    fecha_limite_respuesta = models.DateField(null=True, blank=True)
    respondida = models.BooleanField(default=False)
    archivo = models.FileField(upload_to="regulatorio/observaciones/%Y/%m/", null=True, blank=True)

    class Meta:
        verbose_name = "Observación de autoridad"
        verbose_name_plural = "Observaciones de autoridad"
        ordering = ["-fecha_observacion"]

    def __str__(self):
        return f"Observación {self.expediente.numero_expediente}"


class SubsanacionRegulatoria(ModeloBase):
    observacion = models.ForeignKey(ObservacionAutoridad, on_delete=models.PROTECT, related_name="subsanaciones")
    fecha_respuesta = models.DateField()
    descripcion = models.TextField()
    archivo = models.FileField(upload_to="regulatorio/subsanaciones/%Y/%m/", null=True, blank=True)
    presentado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name="subsanaciones_regulatorias")

    class Meta:
        verbose_name = "Subsanación regulatoria"
        verbose_name_plural = "Subsanaciones regulatorias"
        ordering = ["-fecha_respuesta"]

    def __str__(self):
        return f"Subsanación {self.observacion.expediente.numero_expediente}"
