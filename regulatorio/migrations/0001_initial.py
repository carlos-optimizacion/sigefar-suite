# Generated manually for SIGEFAR Suite PostgreSQL setup

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductoRegulatorio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("activo", models.BooleanField(default=True)),
                ("codigo", models.CharField(max_length=60, unique=True)),
                ("nombre_comercial", models.CharField(max_length=200)),
                ("categoria", models.CharField(choices=[("MEDICAMENTO", "Medicamento"), ("DISPOSITIVO", "Dispositivo médico"), ("COSMETICO", "Cosmético"), ("OTRO", "Otro regulado")], default="MEDICAMENTO", max_length=30)),
                ("principio_activo", models.CharField(blank=True, max_length=255)),
                ("forma_farmaceutica", models.CharField(blank=True, max_length=120)),
                ("concentracion", models.CharField(blank=True, max_length=120)),
                ("presentacion", models.CharField(blank=True, max_length=200)),
                ("titular", models.CharField(blank=True, max_length=200)),
                ("fabricante", models.CharField(blank=True, max_length=200)),
                ("pais_origen", models.CharField(blank=True, max_length=100)),
                ("condiciones_almacenamiento", models.TextField(blank=True)),
                ("condiciones_transporte", models.TextField(blank=True)),
                ("estado_regulatorio", models.CharField(choices=[("EN_EVALUACION", "En evaluación"), ("INSCRITO", "Inscrito"), ("VIGENTE", "Vigente"), ("SUSPENDIDO", "Suspendido"), ("CANCELADO", "Cancelado"), ("NO_VIGENTE", "No vigente")], default="EN_EVALUACION", max_length=30)),
                ("empresa", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="productos_regulatorios", to="core.empresa")),
                ("responsable_regulatorio", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="productos_regulatorios_responsable", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Producto regulatorio",
                "verbose_name_plural": "Productos regulatorios",
                "ordering": ["nombre_comercial", "codigo"],
            },
        ),
        migrations.CreateModel(
            name="ExpedienteDIGEMID",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("activo", models.BooleanField(default=True)),
                ("numero_expediente", models.CharField(max_length=120, unique=True)),
                ("tipo", models.CharField(choices=[("INSCRIPCION", "Inscripción"), ("RENOVACION", "Renovación"), ("REINSCRIPCION", "Reinscripción"), ("MODIFICACION", "Modificación post-registro"), ("ACTUALIZACION", "Actualización"), ("OTRO", "Otro trámite")], max_length=30)),
                ("estado", models.CharField(choices=[("PREPARACION", "Preparación"), ("PRESENTADO", "Presentado"), ("EVALUACION", "En evaluación"), ("OBSERVADO", "Observado"), ("SUBSANADO", "Subsanado"), ("APROBADO", "Aprobado"), ("DENEGADO", "Denegado"), ("CERRADO", "Cerrado")], default="PREPARACION", max_length=30)),
                ("fecha_presentacion", models.DateField(blank=True, null=True)),
                ("fecha_resolucion", models.DateField(blank=True, null=True)),
                ("comentario", models.TextField(blank=True)),
                ("producto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="expedientes", to="regulatorio.productoregulatorio")),
                ("responsable", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="expedientes_regulatorios", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Expediente DIGEMID",
                "verbose_name_plural": "Expedientes DIGEMID",
                "ordering": ["-creado_en"],
            },
        ),
        migrations.CreateModel(
            name="RegistroSanitarioRegulatorio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("activo", models.BooleanField(default=True)),
                ("numero_registro", models.CharField(max_length=120, unique=True)),
                ("fecha_emision", models.DateField(blank=True, null=True)),
                ("fecha_vencimiento", models.DateField(blank=True, null=True)),
                ("estado", models.CharField(choices=[("VIGENTE", "Vigente"), ("POR_VENCER", "Por vencer"), ("VENCIDO", "Vencido"), ("SUSPENDIDO", "Suspendido"), ("CANCELADO", "Cancelado")], default="VIGENTE", max_length=30)),
                ("resolucion", models.FileField(blank=True, null=True, upload_to="regulatorio/resoluciones/%Y/%m/")),
                ("expediente_origen", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="registros_generados", to="regulatorio.expedientedigemid")),
                ("producto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="registros_sanitarios", to="regulatorio.productoregulatorio")),
            ],
            options={
                "verbose_name": "Registro sanitario regulatorio",
                "verbose_name_plural": "Registros sanitarios regulatorios",
                "ordering": ["producto", "numero_registro"],
            },
        ),
        migrations.CreateModel(
            name="DocumentoRegulatorioProducto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("activo", models.BooleanField(default=True)),
                ("tipo", models.CharField(choices=[("FICHA_TECNICA", "Ficha técnica aprobada"), ("INSERTO", "Inserto aprobado"), ("ROTULADO_MEDIATO", "Rotulado mediato"), ("ROTULADO_INMEDIATO", "Rotulado inmediato"), ("CONDICION_ALMACENAMIENTO", "Condición aprobada de almacenamiento"), ("CONDICION_TRANSPORTE", "Condición aprobada de transporte"), ("CERTIFICADO", "Certificado regulatorio"), ("COMUNICACION_AUTORIDAD", "Comunicación de autoridad"), ("SUSTENTO", "Documento de sustento")], max_length=40)),
                ("codigo_documento", models.CharField(blank=True, max_length=80)),
                ("titulo", models.CharField(max_length=255)),
                ("version", models.CharField(blank=True, max_length=30)),
                ("fecha_aprobacion", models.DateField(blank=True, null=True)),
                ("archivo", models.FileField(blank=True, null=True, upload_to="regulatorio/documentos/%Y/%m/")),
                ("observacion", models.TextField(blank=True)),
                ("expediente", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="documentos", to="regulatorio.expedientedigemid")),
                ("producto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="documentos_regulatorios", to="regulatorio.productoregulatorio")),
            ],
            options={
                "verbose_name": "Documento regulatorio del producto",
                "verbose_name_plural": "Documentos regulatorios del producto",
                "ordering": ["producto", "tipo", "-fecha_aprobacion"],
            },
        ),
        migrations.CreateModel(
            name="ObservacionAutoridad",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("activo", models.BooleanField(default=True)),
                ("fecha_observacion", models.DateField()),
                ("descripcion", models.TextField()),
                ("fecha_limite_respuesta", models.DateField(blank=True, null=True)),
                ("respondida", models.BooleanField(default=False)),
                ("archivo", models.FileField(blank=True, null=True, upload_to="regulatorio/observaciones/%Y/%m/")),
                ("expediente", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="observaciones", to="regulatorio.expedientedigemid")),
            ],
            options={
                "verbose_name": "Observación de autoridad",
                "verbose_name_plural": "Observaciones de autoridad",
                "ordering": ["-fecha_observacion"],
            },
        ),
        migrations.CreateModel(
            name="SubsanacionRegulatoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("activo", models.BooleanField(default=True)),
                ("fecha_respuesta", models.DateField()),
                ("descripcion", models.TextField()),
                ("archivo", models.FileField(blank=True, null=True, upload_to="regulatorio/subsanaciones/%Y/%m/")),
                ("observacion", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="subsanaciones", to="regulatorio.observacionautoridad")),
                ("presentado_por", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="subsanaciones_regulatorias", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Subsanación regulatoria",
                "verbose_name_plural": "Subsanaciones regulatorias",
                "ordering": ["-fecha_respuesta"],
            },
        ),
        migrations.AddIndex(model_name="productoregulatorio", index=models.Index(fields=["codigo"], name="regulatorio_codigo_idx")),
        migrations.AddIndex(model_name="productoregulatorio", index=models.Index(fields=["nombre_comercial"], name="regulatorio_nombre_idx")),
        migrations.AddIndex(model_name="productoregulatorio", index=models.Index(fields=["estado_regulatorio"], name="regulatorio_estado_idx")),
        migrations.AddIndex(model_name="expedientedigemid", index=models.Index(fields=["numero_expediente"], name="regulatorio_expediente_idx")),
        migrations.AddIndex(model_name="expedientedigemid", index=models.Index(fields=["estado"], name="regulatorio_exp_estado_idx")),
        migrations.AddIndex(model_name="registrosanitarioregulatorio", index=models.Index(fields=["numero_registro"], name="regulatorio_registro_idx")),
        migrations.AddIndex(model_name="registrosanitarioregulatorio", index=models.Index(fields=["fecha_vencimiento"], name="regulatorio_vencimiento_idx")),
        migrations.AddIndex(model_name="documentoregulatorioproducto", index=models.Index(fields=["tipo"], name="regulatorio_doc_tipo_idx")),
        migrations.AddIndex(model_name="documentoregulatorioproducto", index=models.Index(fields=["codigo_documento"], name="regulatorio_doc_codigo_idx")),
    ]
