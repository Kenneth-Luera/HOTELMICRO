# ============================================================
#  API Gateway — Dockerfile
#  Base: Python 3.11 slim
# ============================================================

FROM python:3.11-slim

# Evita que Python escriba .pyc y bufferiza stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema (necesarias para mysqlclient si lo usas)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Puerto expuesto
EXPOSE 8080

# Comando por defecto (sobreescrito por docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]