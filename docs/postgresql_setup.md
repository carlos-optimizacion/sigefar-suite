# Configuración de PostgreSQL para SIGEFAR Suite

SIGEFAR Suite debe trabajar con PostgreSQL para el entorno real del proyecto. SQLite puede usarse solo como respaldo temporal de desarrollo.

## 1. Crear base y usuario en PostgreSQL

Abrir pgAdmin o psql y ejecutar:

```sql
CREATE DATABASE sigefar_suite
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'Spanish_Peru.1252'
    LC_CTYPE = 'Spanish_Peru.1252'
    TEMPLATE template0;

CREATE USER sigefar_user WITH PASSWORD 'cambia_esta_clave_segura';

ALTER ROLE sigefar_user SET client_encoding TO 'utf8';
ALTER ROLE sigefar_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sigefar_user SET timezone TO 'America/Lima';

GRANT ALL PRIVILEGES ON DATABASE sigefar_suite TO sigefar_user;
```

Si PostgreSQL no acepta `Spanish_Peru.1252`, crear la base desde pgAdmin usando codificación `UTF8` y los valores regionales disponibles en la instalación local.

## 2. Crear archivo `.env`

Copiar `.env.example` como `.env` en la raíz del proyecto y ajustar:

```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=sigefar_suite
DATABASE_USER=sigefar_user
DATABASE_PASSWORD=cambia_esta_clave_segura
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_CONN_MAX_AGE=60
DATABASE_SSLMODE=
```

El archivo `.env` no debe subirse a GitHub.

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

El proyecto ya usa `psycopg[binary]` para conexión con PostgreSQL.

## 4. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 5. Validar conexión

Abrir:

```text
http://127.0.0.1:8000/admin/
```

Luego validar:

```text
/admin/core/empresa/
/admin/core/sedeempresa/
/admin/regulatorio/
```

## 6. Nota de gobierno de datos

- Core mantiene empresas, usuarios, roles, licencias, parámetros y seguridad.
- Regulatorio gobierna productos regulatorios, expedientes y documentos regulatorios del producto.
- QMS gobierna documentos del SGI, desviaciones, CAPA, riesgos, auditorías y capacitaciones.
- BPA, BPDT y BPFV mantienen datos especializados sin reemplazar ERP, WMS ni TMS.
