from django.shortcuts import render


def dashboard(request):
    modulos = [
        {
            'codigo': 'CORE',
            'nombre': 'SIGEFAR-Core',
            'descripcion': 'Usuarios, roles, permisos, productos, licencias, adjuntos y configuración general.',
            'estado': 'Base obligatoria',
            'icono': 'C',
        },
        {
            'codigo': 'QMS',
            'nombre': 'SIGEFAR-QMS / Calidad',
            'descripcion': 'Documentos, registros sanitarios, desviaciones, CAPA, auditorías y evidencias.',
            'estado': 'Módulo rector',
            'icono': 'Q',
        },
        {
            'codigo': 'BPA',
            'nombre': 'SIGEFAR-BPA',
            'descripcion': 'Control regulatorio de almacenamiento, zonas, excursiones y lotes BPA.',
            'estado': 'Adicional',
            'icono': 'A',
        },
        {
            'codigo': 'BPDT',
            'nombre': 'SIGEFAR-BPDT',
            'descripcion': 'Buenas prácticas de distribución y transporte desde enfoque regulatorio.',
            'estado': 'Adicional',
            'icono': 'T',
        },
        {
            'codigo': 'BPFV',
            'nombre': 'SIGEFAR-BPFV',
            'descripcion': 'Farmacovigilancia, casos, eventos adversos, seguimiento y señales de seguridad.',
            'estado': 'Adicional',
            'icono': 'P',
        },
    ]

    indicadores = [
        {'valor': '5', 'etiqueta': 'Módulos regulados'},
        {'valor': '1', 'etiqueta': 'Core común'},
        {'valor': '100%', 'etiqueta': 'CAPA centralizada en QMS'},
        {'valor': '0', 'etiqueta': 'Duplicidad de lotes maestros'},
    ]

    return render(request, 'core/dashboard.html', {'modulos': modulos, 'indicadores': indicadores})
