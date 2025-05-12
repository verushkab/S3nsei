# Imagen base
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /Bot

# Copia todos los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el bot
CMD ["python", "run.py"]
