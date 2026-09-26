# =====================================================================
# STAGE 1: BUILDER
# =====================================================================
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.0.0

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /build

COPY pyproject.toml poetry.lock ./

# Instalamos solo dependencias de producción
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

# =====================================================================
# STAGE 2: PRODUCTION
# =====================================================================
FROM python:3.12-slim AS production

WORKDIR /app

# 1. Traemos librerías del builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 2. Copiamos nuestro código fuente y secretos (El .env debe manejarse distinto en prod real)
COPY app /app/app
COPY .env /app/.env

# 3. Hardening (Endurecimiento sin root)
RUN useradd -m appuser
USER appuser

EXPOSE 8000

# 4. Arrancamos Uvicorn apuntando a nuestro main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]