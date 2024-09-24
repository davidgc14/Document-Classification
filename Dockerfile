FROM python:3.12-slim

COPY . /app
WORKDIR /app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN mkdir -p /app/logs
RUN pip install -r requirements.txt

VOLUME /app/logs

CMD ["python3", "app/main.py"]