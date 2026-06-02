from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class ModeloBase(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Empresa(ModeloBase):
    ruc = models.CharField(max_length=20, unique=True)
    razon_social = models.CharField(max_length=200)
    nombre_comercial = models.CharField(max_length=200, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=100, default="Perú")

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["razon_social"]

    def __str__(self):
        return self.razon_social


class Usuario(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True, blank=True, related_name="usuarios")
    cargo = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=40, blank=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class ModuloSistema(ModeloBase):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    obligatorio = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Módulo del sistema"
        verbose_name_plural = "Módulos del sistema"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class LicenciaModulo(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="licencias")
    modulo = models.ForeignKey(ModuloSistema, on_delete=models.PROTECT, related_name="licencias")
    fecha_inicio = models.DateField(default=timezone.localdate)
    fecha_fin = models.DateField(null=True, blank=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Licencia de módulo"
        verbose_name_plural = "Licencias de módulos"
        unique_together = [("empresa", "modulo")]

    def __str__(self):
        return f"{self.empresa} - {self.modulo.codigo}"


class Producto(ModeloBase):
    ESTADOS = [("ACTIVO", "Activo"), ("INACTIVO", "Inactivo"), ("SUSPENDIDO", "Suspendido")]
    codigo = models.CharField(max_length=60, unique=True)
    nombre_comercial = models.CharField(max_length=200)
    principio_activo = models.CharField(max_length=255)
    forma_farmaceutica = models.CharField(max_length=120)
    concentracion = models.CharField(max_length=120)
    presentacion = models.CharField(max_length=200)
    titular = models.CharField(max_length=200)
    fabricante = models.CharField(max_length=200)
    pais_origen = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="ACTIVO")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre_comercial"]
        indexes = [models.Index(fields=["codigo"]), models.Index(fields=["nombre_comercial"])]

    def __str__(self):
        return f"{self.codigo} - {self.nombre_comercial}"


class ArchivoAdjunto(ModeloBase):
    modulo_origen = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=255)
    archivo = models.FileField(upload_to="adjuntos/%Y/%m/")
    subido_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="adjuntos")

    class Meta:
        verbose_name = "Archivo adjunto"
        verbose_name_plural = "Archivos adjuntos"
        ordering = ["-creado_en"]

    def __str__(self):
        return self.descripcion


class ParametroGeneral(ModeloBase):
    clave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Parámetro general"
        verbose_name_plural = "Parámetros generales"
        ordering = ["clave"]

    def __str__(self):
        return self.clave


class Notificacion(ModeloBase):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones")
    titulo = models.CharField(max_length=180)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ["-creado_en"]

    def __str__(self):
        return self.titulo
