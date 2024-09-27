FROM python:3.12-slim

# Instalar Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# COPY . /app # Esto solo para produccion
WORKDIR /app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# RUN mkdir -p /app/logs # Esto cuando no se monte la aplicacion entera como volumen
# requirements solo copiado para dev, si no se copia el proyecto entero
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /app/logs

CMD ["python3", "src/main.py"]