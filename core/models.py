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
    TIPOS_EMPRESA = [
        ("DROGUERIA", "Droguería"),
        ("LABORATORIO", "Laboratorio"),
        ("DISTRIBUIDORA", "Distribuidora"),
        ("IMPORTADORA", "Importadora"),
        ("TITULAR_RS", "Titular de registro sanitario"),
        ("CONSULTORA", "Consultora regulatoria"),
        ("OTRA", "Otra"),
    ]
    TIPOS_INSTALACION = [
        ("LOCAL", "Servidor local / red interna"),
        ("HOST_CLIENTE", "Host propio del cliente"),
        ("VPS", "VPS privado"),
        ("NUBE", "Nube"),
        ("HIBRIDO", "Híbrido"),
    ]
    ESTADOS_OPERATIVOS = [
        ("IMPLEMENTACION", "En implementación"),
        ("ACTIVA", "Activa"),
        ("SUSPENDIDA", "Suspendida"),
        ("INACTIVA", "Inactiva"),
    ]

    ruc = models.CharField(max_length=20, unique=True)
    razon_social = models.CharField(max_length=200)
    nombre_comercial = models.CharField(max_length=200, blank=True)
    tipo_empresa = models.CharField(max_length=30, choices=TIPOS_EMPRESA, default="DROGUERIA")
    representante_legal = models.CharField(max_length=200, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=120, blank=True)
    pais = models.CharField(max_length=100, default="Perú")
    email_contacto = models.EmailField(blank=True)
    telefono_contacto = models.CharField(max_length=40, blank=True)
    responsable_sistema = models.CharField(max_length=180, blank=True)
    tipo_instalacion = models.CharField(max_length=30, choices=TIPOS_INSTALACION, default="HOST_CLIENTE")
    dominio_sistema = models.CharField(max_length=180, blank=True, help_text="Dominio, IP o referencia interna donde opera SIGEFAR para esta empresa.")
    estado_operativo = models.CharField(max_length=30, choices=ESTADOS_OPERATIVOS, default="IMPLEMENTACION")
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["razon_social"]
        indexes = [models.Index(fields=["ruc"]), models.Index(fields=["estado_operativo"]), models.Index(fields=["tipo_empresa"])]

    def __str__(self):
        return self.razon_social


class SedeEmpresa(ModeloBase):
    TIPOS_SEDE = [
        ("OFICINA_REGULATORIA", "Oficina regulatoria"),
        ("ALMACEN", "Almacén"),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="sedes")
    codigo = models.CharField(max_length=60)
    nombre = models.CharField(max_length=180)
    tipo_sede = models.CharField(max_length=30, choices=TIPOS_SEDE, default="OFICINA_REGULATORIA")
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=120, blank=True)
    pais = models.CharField(max_length=100, default="Perú")
    responsable_contacto = models.CharField(max_length=180, blank=True)
    email_contacto = models.EmailField(blank=True)
    telefono_contacto = models.CharField(max_length=40, blank=True)
    observaciones = models.TextField(blank=True, help_text="En Core la sede es referencia base. El control regulado de almacenes BPA se gestiona en SIGEFAR-BPA.")

    class Meta:
        verbose_name = "Sede de empresa"
        verbose_name_plural = "Sedes de empresa"
        unique_together = [("empresa", "codigo")]
        ordering = ["empresa__razon_social", "codigo"]
        indexes = [models.Index(fields=["codigo"]), models.Index(fields=["tipo_sede"])]

    def __str__(self):
        return f"{self.empresa} - {self.codigo}"


class Cargo(ModeloBase):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)
    nivel = models.CharField(max_length=80, blank=True, help_text="Ejemplo: Responsable, Asistente, Revisor, Aprobador, Auditor.")

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True, blank=True, related_name="usuarios")
    cargo = models.CharField(max_length=120, blank=True, help_text="Campo heredado. Usar cargo funcional para nuevas asignaciones.")
    cargo_funcional = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=True, blank=True, related_name="usuarios")
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


class RolFuncional(ModeloBase):
    NIVELES = [
        ("RESPONSABLE", "Responsable"),
        ("ASISTENTE", "Asistente"),
        ("REVISOR", "Revisor"),
        ("APROBADOR", "Aprobador"),
        ("AUDITOR", "Auditor / Consulta"),
        ("ADMINISTRADOR", "Administrador"),
    ]
    modulo = models.ForeignKey(ModuloSistema, on_delete=models.PROTECT, related_name="roles_funcionales")
    nombre = models.CharField(max_length=140)
    nivel = models.CharField(max_length=30, choices=NIVELES, default="ASISTENTE")
    descripcion = models.TextField(blank=True)
    puede_ver = models.BooleanField(default=True)
    puede_crear = models.BooleanField(default=False)
    puede_editar = models.BooleanField(default=False)
    puede_aprobar = models.BooleanField(default=False)
    puede_cerrar = models.BooleanField(default=False)
    puede_exportar = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Rol funcional"
        verbose_name_plural = "Roles funcionales"
        unique_together = [("modulo", "nombre")]
        ordering = ["modulo__codigo", "nivel", "nombre"]

    def __str__(self):
        return f"{self.modulo.codigo} - {self.nombre}"


class AsignacionRolUsuario(ModeloBase):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="roles_sigefar")
    rol = models.ForeignKey(RolFuncional, on_delete=models.PROTECT, related_name="usuarios_asignados")
    asignado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name="roles_asignados")
    fecha_inicio = models.DateField(default=timezone.localdate)
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Asignación de rol"
        verbose_name_plural = "Asignaciones de roles"
        unique_together = [("usuario", "rol")]
        ordering = ["usuario__username", "rol__modulo__codigo"]

    def __str__(self):
        return f"{self.usuario} - {self.rol}"


class LicenciaModulo(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="licencias")
    modulo = models.ForeignKey(ModuloSistema, on_delete=models.PROTECT, related_name="licencias")
    fecha_inicio = models.DateField(default=timezone.localdate)
    fecha_fin = models.DateField(null=True, blank=True)
    habilitado = models.BooleanField(default=True)
    clave_local = models.CharField(max_length=255, blank=True, help_text="Clave o referencia local para instalaciones on-premise.")

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
        verbose_name = "Producto legado de Core"
        verbose_name_plural = "Productos legados de Core"
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


class BitacoraAccion(ModeloBase):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name="acciones_bitacora")
    modulo = models.CharField(max_length=30)
    accion = models.CharField(max_length=120)
    modelo = models.CharField(max_length=120, blank=True)
    objeto_id = models.CharField(max_length=80, blank=True)
    resumen = models.TextField()
    valor_anterior = models.TextField(blank=True)
    valor_nuevo = models.TextField(blank=True)
    ip_origen = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = "Bitácora de acción"
        verbose_name_plural = "Bitácora de acciones"
        ordering = ["-creado_en"]
        indexes = [models.Index(fields=["modulo"]), models.Index(fields=["accion"]), models.Index(fields=["creado_en"])]

    def __str__(self):
        return f"{self.modulo} - {self.accion} - {self.creado_en:%Y-%m-%d %H:%M}"
