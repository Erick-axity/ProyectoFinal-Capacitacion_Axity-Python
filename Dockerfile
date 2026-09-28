# =====================================================================
# STAGE 1: BUILDER
# =====================================================================
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.0.0

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /build

# 1. Copiamos SOLO el TOML para evitar los choques del poetry.lock entre OS
COPY pyproject.toml ./

# 2. Instalamos las dependencias de producción desde cero
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

# =====================================================================
# STAGE 2: PRODUCTION
# =====================================================================
FROM python:3.12-slim AS production

WORKDIR /app

# 1. Traemos las librerías pre-instaladas del Builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 2. Copiamos nuestro código fuente (el núcleo Hexagonal)
COPY app /app/app

# 3. Copiamos el sistema de Migraciones (Alembic)
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini

# Opcional: Si tienes tu archivo .env con variables de producción
COPY .env /app/.env

# 4. Hardening y Permisos para SQLite
# Creamos al usuario 'myuser' y le hacemos dueño de /app para que pueda crear el archivo .sqlite
RUN useradd -m myuser && chown -R myuser /app
USER myuser

EXPOSE 8000

# 5. El Script de Arranque (Migrar y Encender)
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]