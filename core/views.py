from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bpa.models import ExcursionBPA, LoteBPA
from bpdt.models import IncidenteTransporte, Transportista, VehiculoAutorizado
from bpfv.models import CasoFarmacovigilancia
from qms.models import CAPA, Desviacion, DocumentoControlado, RegistroSanitario
from .models import LicenciaModulo, Producto


MODULES = [
    {
        "slug": "core",
        "codigo": "CORE",
        "nombre": "SIGEFAR-Core",
        "titulo": "Núcleo común de la plataforma",
        "descripcion": "Administra la base común de usuarios, seguridad, productos, permisos y trazabilidad transversal de la suite.",
        "mensaje": "Core sostiene la operación común de SIGEFAR Suite y garantiza seguridad, trazabilidad y datos maestros compartidos.",
        "etiqueta": "Núcleo común",
        "icono": "◈",
        "componentes": [
            "Usuarios y perfiles",
            "Roles y permisos",
            "Maestro de productos",
            "Bitácora general",
            "Adjuntos y notificaciones",
            "Parámetros generales",
        ],
        "principios": [
            "Control de acceso por perfil",
            "Datos maestros compartidos",
            "Trazabilidad transversal",
            "Seguridad común para todos los módulos",
        ],
    },
    {
        "slug": "qms",
        "codigo": "QMS",
        "nombre": "SIGEFAR-QMS / Calidad",
        "titulo": "Gestión de calidad y cumplimiento documental",
        "descripcion": "Módulo rector de calidad. Centraliza documentos, auditorías, hallazgos, desviaciones, CAPA, riesgos y evidencia para inspecciones regulatorias.",
        "mensaje": "QMS gobierna la calidad, los documentos, las desviaciones, las CAPA y la mejora continua.",
        "etiqueta": "Módulo rector",
        "icono": "✦",
        "destacado": True,
        "componentes": [
            "Documentos controlados",
            "Lista maestra documental",
            "Registros sanitarios",
            "Fichas técnicas, insertos y rotulados",
            "Auditorías y hallazgos",
            "Desviaciones y CAPA",
            "Riesgos y control de cambios",
            "Capacitaciones y verificación de eficacia",
        ],
        "principios": [
            "Gobierno documental centralizado",
            "CAPA única desde Calidad",
            "Evidencia para auditorías e inspecciones",
            "Mejora continua trazable",
        ],
    },
    {
        "slug": "bpa",
        "codigo": "BPA",
        "nombre": "SIGEFAR-BPA",
        "titulo": "Buenas Prácticas de Almacenamiento",
        "descripcion": "Controla el cumplimiento regulatorio del almacenamiento, condiciones ambientales, evidencias, excursiones y estados regulatorios de lotes.",
        "mensaje": "BPA controla el cumplimiento regulatorio del almacenamiento sin administrar inventario operativo.",
        "etiqueta": "Módulo adicional",
        "icono": "▣",
        "componentes": [
            "Almacenes y zonas reguladas",
            "Cuarentena, aprobado, rechazado y devoluciones",
            "Temperatura y humedad",
            "Excursiones ambientales",
            "Limpieza y control de plagas",
            "Equipos críticos, mantenimiento y calibración",
            "Autoinspecciones y evidencias BPA",
            "Control regulatorio de lotes BPA",
        ],
        "principios": [
            "Control regulatorio de estado de lote",
            "Evidencia ambiental y documental",
            "Derivación de incumplimientos a QMS",
            "Consulta posterior desde BPFV según permisos",
        ],
    },
    {
        "slug": "bpdt",
        "codigo": "BPDT",
        "nombre": "SIGEFAR-BPDT",
        "titulo": "Buenas Prácticas de Distribución y Transporte",
        "descripcion": "Gestiona la evidencia regulatoria del transporte, condiciones de conservación en tránsito, incidentes y devoluciones con impacto en calidad.",
        "mensaje": "BPDT controla la evidencia regulatoria de distribución y transporte sin administrar planificación logística operativa.",
        "etiqueta": "Módulo adicional",
        "icono": "⬡",
        "componentes": [
            "Transportistas autorizados",
            "Vehículos autorizados",
            "Conductores, si aplica",
            "Documentación de transporte",
            "Conservación en tránsito",
            "Excursiones e incidentes",
            "Devoluciones y entregas fallidas",
            "Evidencias de entrega con impacto en calidad",
        ],
        "principios": [
            "Cumplimiento regulatorio del transporte",
            "Trazabilidad de incidentes en tránsito",
            "Evidencia de conservación y entrega",
            "Derivación de incumplimientos a QMS",
        ],
    },
    {
        "slug": "bpfv",
        "codigo": "BPFV",
        "nombre": "SIGEFAR-BPFV",
        "titulo": "Farmacovigilancia y BPFV",
        "descripcion": "Permite registrar, evaluar y dar seguimiento a casos de farmacovigilancia, vinculando productos y lotes reportados cuando corresponda.",
        "mensaje": "BPFV gestiona farmacovigilancia y puede consultar lotes BPA vinculados sin modificar su estado regulatorio.",
        "etiqueta": "Módulo adicional",
        "icono": "✚",
        "componentes": [
            "Registro de casos",
            "Sospechas de RAM y eventos adversos",
            "Errores de medicación",
            "Falta de eficacia y PRM",
            "Gravedad y causalidad",
            "Seguimiento y reportes regulatorios",
            "Señales de seguridad",
            "Consulta de lotes BPA",
        ],
        "principios": [
            "Registro trazable de casos",
            "Validación de datos mínimos",
            "Consulta controlada de lotes BPA",
            "Escalamiento de hallazgos a QMS",
        ],
    },
]


PRINCIPLES = [
    {
        "titulo": "Trazabilidad",
        "descripcion": "Toda acción relevante debe quedar registrada para auditoría y revisión posterior.",
        "icono": "⌁",
    },
    {
        "titulo": "Control documental",
        "descripcion": "Los documentos mantienen versión, vigencia, aprobación, historial y responsable.",
        "icono": "☷",
    },
    {
        "titulo": "Seguridad por roles",
        "descripcion": "Cada usuario accede solo a funciones y registros autorizados por su perfil.",
        "icono": "◉",
    },
    {
        "titulo": "Evidencia regulatoria",
        "descripcion": "Los registros sustentan auditorías, inspecciones, seguimiento interno y mejora continua.",
        "icono": "✓",
    },
]


FLOW_STEPS = [
    "Producto maestro",
    "Documentos regulatorios vigentes",
    "BPA / BPDT / BPFV",
    "Hallazgos, incidentes o señales",
    "QMS / Calidad",
    "CAPA y cierre eficaz",
]


def home(request):
    qms_module = next(module for module in MODULES if module["slug"] == "qms")
    secondary_modules = [module for module in MODULES if module["slug"] != "qms"]
    return render(
        request,
        "core/dashboard.html",
        {
            "qms_module": qms_module,
            "secondary_modules": secondary_modules,
            "principles": PRINCIPLES,
            "flow_steps": FLOW_STEPS,
        },
    )


def module_detail(request, slug):
    selected_module = next((module for module in MODULES if module["slug"] == slug), None)
    if selected_module is None:
        selected_module = next(module for module in MODULES if module["slug"] == "qms")

    related_modules = [module for module in MODULES if module["slug"] != selected_module["slug"]]
    return render(
        request,
        "core/module_detail.html",
        {
            "module": selected_module,
            "related_modules": related_modules,
        },
    )


@login_required
def panel(request):
    empresa = getattr(request.user, "empresa", None)
    licencias = []
    if empresa:
        licencias = list(
            LicenciaModulo.objects.select_related("modulo")
            .filter(empresa=empresa, habilitado=True)
            .order_by("modulo__codigo")
        )

    resumen = [
        {
            "codigo": "CORE",
            "titulo": "Datos maestros",
            "valor": Producto.objects.filter(activo=True).count(),
            "detalle": "Productos activos registrados en Core",
            "url": "/admin/core/producto/",
        },
        {
            "codigo": "QMS",
            "titulo": "Documentos vigentes",
            "valor": DocumentoControlado.objects.filter(estado="VIGENTE", activo=True).count(),
            "detalle": "Documentos controlados con estado vigente",
            "url": "/admin/qms/documentocontrolado/",
        },
        {
            "codigo": "QMS",
            "titulo": "Desviaciones abiertas",
            "valor": Desviacion.objects.exclude(estado="CERRADA").filter(activo=True).count(),
            "detalle": "Desviaciones pendientes de investigación o cierre",
            "url": "/admin/qms/desviacion/",
        },
        {
            "codigo": "QMS",
            "titulo": "CAPA en seguimiento",
            "valor": CAPA.objects.exclude(estado="CERRADA").filter(activo=True).count(),
            "detalle": "Acciones correctivas/preventivas gestionadas desde Calidad",
            "url": "/admin/qms/capa/",
        },
        {
            "codigo": "BPA",
            "titulo": "Lotes BPA controlados",
            "valor": LoteBPA.objects.filter(activo=True).count(),
            "detalle": "Lotes registrados con finalidad regulatoria BPA",
            "url": "/admin/bpa/lotebpa/",
        },
        {
            "codigo": "BPFV",
            "titulo": "Casos BPFV abiertos",
            "valor": CasoFarmacovigilancia.objects.exclude(estado="CERRADO").filter(activo=True).count(),
            "detalle": "Casos de farmacovigilancia en gestión",
            "url": "/admin/bpfv/casofarmacovigilancia/",
        },
    ]

    workstreams = [
        {
            "codigo": "QMS",
            "titulo": "Calidad y CAPA",
            "descripcion": "Gestionar documentos, registros sanitarios, desviaciones y CAPA centralizadas.",
            "registros": [
                f"{RegistroSanitario.objects.filter(activo=True).count()} registros sanitarios",
                f"{Desviacion.objects.exclude(estado='CERRADA').filter(activo=True).count()} desviaciones abiertas",
                f"{CAPA.objects.exclude(estado='CERRADA').filter(activo=True).count()} CAPA en proceso",
            ],
            "url": "/admin/qms/",
        },
        {
            "codigo": "BPA",
            "titulo": "Almacenamiento regulatorio",
            "descripcion": "Controlar lotes BPA, excursiones, evidencias y estados regulatorios de almacenamiento.",
            "registros": [
                f"{LoteBPA.objects.filter(activo=True).count()} lotes BPA",
                f"{ExcursionBPA.objects.filter(activo=True).count()} excursiones BPA",
            ],
            "url": "/admin/bpa/",
        },
        {
            "codigo": "BPDT",
            "titulo": "Distribución y transporte regulatorio",
            "descripcion": "Supervisar transportistas, vehículos autorizados e incidentes con impacto en calidad.",
            "registros": [
                f"{Transportista.objects.filter(autorizado=True, activo=True).count()} transportistas autorizados",
                f"{VehiculoAutorizado.objects.filter(autorizado=True, activo=True).count()} vehículos autorizados",
                f"{IncidenteTransporte.objects.filter(activo=True).count()} incidentes BPDT",
            ],
            "url": "/admin/bpdt/",
        },
        {
            "codigo": "BPFV",
            "titulo": "Farmacovigilancia",
            "descripcion": "Registrar casos, seguimiento, gravedad, causalidad y consulta de lotes BPA vinculados.",
            "registros": [
                f"{CasoFarmacovigilancia.objects.exclude(estado='CERRADO').filter(activo=True).count()} casos abiertos",
                f"{CasoFarmacovigilancia.objects.filter(lote_no_encontrado_bpa=True, activo=True).count()} casos con lote no encontrado en BPA",
            ],
            "url": "/admin/bpfv/",
        },
    ]

    return render(
        request,
        "core/panel.html",
        {
            "empresa": empresa,
            "licencias": licencias,
            "resumen": resumen,
            "workstreams": workstreams,
        },
    )


# Alias temporal para compatibilidad con versiones previas.
dashboard = home
