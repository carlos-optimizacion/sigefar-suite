from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bpa.models import ExcursionBPA, LoteBPA
from bpdt.models import IncidenteTransporte, Transportista, VehiculoAutorizado
from bpfv.models import CasoFarmacovigilancia
from qms.models import CAPA, Desviacion, DocumentoControlado
from regulatorio.models import ExpedienteDIGEMID, ProductoRegulatorio, RegistroSanitarioRegulatorio
from .models import LicenciaModulo


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
            "codigo": "REG",
            "titulo": "Productos regulatorios",
            "valor": ProductoRegulatorio.objects.filter(activo=True).count(),
            "detalle": "Productos creados y gobernados desde Regulatorio",
            "url": "/admin/regulatorio/productoregulatorio/",
        },
        {
            "codigo": "REG",
            "titulo": "Registros sanitarios",
            "valor": RegistroSanitarioRegulatorio.objects.filter(activo=True).count(),
            "detalle": "Registros sanitarios controlados por producto regulatorio",
            "url": "/admin/regulatorio/registrosanitarioregulatorio/",
        },
        {
            "codigo": "QMS",
            "titulo": "Documentos SGI vigentes",
            "valor": DocumentoControlado.objects.filter(estado="VIGENTE", activo=True).count(),
            "detalle": "Documentos del Sistema de Gestión Integrado",
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
            "detalle": "Lotes asociados a productos regulatorios",
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
            "codigo": "REG",
            "titulo": "Gestión regulatoria del producto",
            "descripcion": "Crear productos regulatorios, expedientes DIGEMID, registros sanitarios, documentos regulatorios, observaciones y subsanaciones.",
            "registros": [
                f"{ProductoRegulatorio.objects.filter(activo=True).count()} productos regulatorios",
                f"{ExpedienteDIGEMID.objects.exclude(estado='CERRADO').filter(activo=True).count()} expedientes abiertos",
                f"{RegistroSanitarioRegulatorio.objects.filter(activo=True).count()} registros sanitarios",
            ],
            "url": "/admin/regulatorio/",
        },
        {
            "codigo": "QMS",
            "titulo": "Calidad y CAPA",
            "descripcion": "Gestionar documentos del SGI, desviaciones, CAPA, auditorías, riesgos, cambios y eficacia.",
            "registros": [
                f"{DocumentoControlado.objects.filter(activo=True).count()} documentos SGI",
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
dashboard = panel
