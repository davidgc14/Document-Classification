FROM python:3.12-slim

# COPY . /app # Esto solo para produccion
# requirements solo copiado para dev, si no se copia el proyecto entero
COPY requirements.txt /app
WORKDIR /app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# RUN mkdir -p /app/logs # Esto cuando no se monte la aplicacion entera como volumen

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /app/logs

CMD ["python3", "app/main.py"]