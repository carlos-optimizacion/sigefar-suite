# SIGEFAR Suite

Plataforma modular para cumplimiento regulatorio, calidad, buenas prácticas y farmacovigilancia.

Arquitectura base: Django + PostgreSQL/SQLite local + monolito modular.

Módulos previstos:

- SIGEFAR-Core
- SIGEFAR-QMS / Calidad
- SIGEFAR-BPA
- SIGEFAR-BPDT
- SIGEFAR-BPFV
- Auditoría
- Reportes

Este repositorio será construido progresivamente bajo reglas de gobierno: Core sostiene la plataforma, QMS gobierna calidad y CAPA, BPA controla almacenamiento regulatorio sin convertirse en WMS, BPDT controla distribución regulatoria sin convertirse en TMS, y BPFV gestiona farmacovigilancia sin administrar lotes ni documentos regulatorios.
