from django.shortcuts import render


def dashboard(request):
    modulos = [
        {
            'codigo': 'CORE',
            'nombre': 'SIGEFAR-Core',
            'descripcion': 'Núcleo común obligatorio de la plataforma. Sostiene seguridad, datos maestros, trazabilidad y configuración general.',
            'estado': 'Base obligatoria',
            'icono': 'C',
            'componentes': [
                'Usuarios, roles y permisos',
                'Autenticación y seguridad',
                'Maestro de productos',
                'Licenciamiento modular',
                'Parámetros generales',
                'Adjuntos, notificaciones y bitácora base',
            ],
        },
        {
            'codigo': 'QMS',
            'nombre': 'SIGEFAR-QMS / Calidad',
            'descripcion': 'Módulo rector de calidad. Gobierna documentos, desviaciones, CAPA, auditorías, riesgos y mejora continua.',
            'estado': 'Módulo rector',
            'icono': 'Q',
            'componentes': [
                'Gestión documental y lista maestra',
                'Registros sanitarios y documentos regulatorios',
                'Fichas técnicas, insertos y rotulados',
                'Desviaciones, hallazgos y auditorías',
                'CAPA centralizada y verificación de eficacia',
                'Riesgos, control de cambios y capacitaciones',
            ],
        },
        {
            'codigo': 'BPA',
            'nombre': 'SIGEFAR-BPA',
            'descripcion': 'Control regulatorio de almacenamiento. No gestiona inventario operativo ni funciones WMS.',
            'estado': 'Módulo adicional',
            'icono': 'A',
            'componentes': [
                'Almacenes y zonas reguladas',
                'Cuarentena, aprobado, rechazado y devoluciones',
                'Temperatura, humedad y excursiones',
                'Limpieza, plagas, mantenimiento y calibración',
                'Autoinspecciones y evidencias BPA',
                'Control regulatorio de lotes BPA',
            ],
        },
        {
            'codigo': 'BPDT',
            'nombre': 'SIGEFAR-BPDT',
            'descripcion': 'Control regulatorio de distribución y transporte. No optimiza rutas ni administra flota como TMS.',
            'estado': 'Módulo adicional',
            'icono': 'T',
            'componentes': [
                'Transportistas autorizados',
                'Vehículos y conductores si aplica',
                'Documentación de transporte',
                'Condiciones de conservación en tránsito',
                'Excursiones e incidentes de transporte',
                'Devoluciones y entregas fallidas con impacto en calidad',
            ],
        },
        {
            'codigo': 'BPFV',
            'nombre': 'SIGEFAR-BPFV',
            'descripcion': 'Farmacovigilancia y buenas prácticas de farmacovigilancia. Registra casos y consulta información regulatoria.',
            'estado': 'Módulo adicional',
            'icono': 'P',
            'componentes': [
                'Registro de casos y sospechas de RAM',
                'Eventos adversos y errores de medicación',
                'Falta de eficacia y problemas relacionados con medicamentos',
                'Validación de datos mínimos, gravedad y causalidad',
                'Seguimiento, reportes regulatorios y señales',
                'Consulta de lotes BPA sin modificar estados',
            ],
        },
    ]

    indicadores = [
        {'valor': '5', 'etiqueta': 'Módulos principales'},
        {'valor': '1', 'etiqueta': 'Core común obligatorio'},
        {'valor': 'QMS', 'etiqueta': 'Gobierno de CAPA y documentos'},
        {'valor': 'BPA', 'etiqueta': 'Lote como dato regulatorio'},
    ]

    return render(request, 'core/dashboard.html', {'modulos': modulos, 'indicadores': indicadores})
