# Usa una imagen de Python oficial
FROM python:3.12-slim

# Instala libmagic y otras dependencias necesarias
RUN apt-get update && \
    apt-get install -y libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala la aplicación en modo editable
RUN pip install --editable .

# Define el comando por defecto cuando se inicie el contenedor
ENTRYPOINT ["rag-code"]