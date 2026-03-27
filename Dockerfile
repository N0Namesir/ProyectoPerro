# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Instalamos dependencias del sistema para que Python hable con PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos el archivo de librerías (si no tienes requirements.txt, mira el paso abajo)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Ejecutamos el archivo principal de tu app
CMD ["python", "main.py"]