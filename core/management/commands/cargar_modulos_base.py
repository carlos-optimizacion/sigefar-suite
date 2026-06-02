from django.core.management.base import BaseCommand

from core.models import ModuloSistema


class Command(BaseCommand):
    help = 'Carga modulos base de SIGEFAR Suite.'

    def handle(self, *args, **options):
        modulos = [
            ('CORE', 'SIGEFAR-Core', 'Nucleo comun obligatorio.', True),
            ('QMS', 'SIGEFAR-QMS Calidad', 'Gestion documental, calidad, desviaciones y CAPA.', True),
            ('BPA', 'SIGEFAR-BPA', 'Buenas Practicas de Almacenamiento con enfoque regulatorio.', False),
            ('BPDT', 'SIGEFAR-BPDT', 'Buenas Practicas de Distribucion y Transporte con enfoque regulatorio.', False),
            ('BPFV', 'SIGEFAR-BPFV', 'Farmacovigilancia y BPFV.', False),
        ]

        for codigo, nombre, descripcion, obligatorio in modulos:
            obj, creado = ModuloSistema.objects.update_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'obligatorio': obligatorio,
                    'activo': True,
                },
            )
            estado = 'creado' if creado else 'actualizado'
            self.stdout.write(self.style.SUCCESS(f'{codigo} {estado}'))
