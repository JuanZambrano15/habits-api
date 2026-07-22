# ---------- ETAPA 1: builder ----------
FROM python:3.14-slim AS builder

# Herramientas de compilación necesarias SOLO para instalar dependencias
# (psycopg2-binary y otras pueden necesitar compilar extensiones en C).
# No estarán en la imagen final.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos solo requirements.txt primero (no todo el código) para
# aprovechar el cache de capas de Docker: si el código cambia pero
# las dependencias no, Docker no vuelve a reinstalar todo desde cero.
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---------- ETAPA 2: imagen final ----------
FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Creamos el usuario ANTES de copiar nada, para que /home/appuser
# ya sea de su propiedad desde el inicio (evita el problema de permisos).
RUN useradd --create-home appuser

WORKDIR /app

# Copiamos los paquetes a la carpeta personal de appuser, NO a /root/.local
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]