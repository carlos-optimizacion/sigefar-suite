from django.shortcuts import render


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


# Alias temporal para compatibilidad con versiones previas.
dashboard = home
