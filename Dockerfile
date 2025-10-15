FROM python:3.11-slim

# Evita bytecode y buffer en logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependencias del sistema (para pandas/pyarrow) y limpia
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# Dependencias Python
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY app.py /app/app.py

# Crea dirs de datos por defecto
RUN mkdir -p /data /out

# Entrada por defecto (se puede sobreescribir con args)
ENTRYPOINT ["python", "/app/app.py"]
CMD ["--input", "/data/input.json", "--output", "/out/stats.json"]