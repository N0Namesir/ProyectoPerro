    # Usamos una imagen base con herramientas de compilación
FROM gcc:latest

# Instalamos CMake y la librería de desarrollo de PostgreSQL
RUN apt-get update && apt-get install -y cmake libpq-dev libpqxx-dev

# Directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copiamos los archivos del proyecto al contenedor
COPY . .

# Creamos la carpeta de build y compilamos
RUN mkdir build && cd build && cmake .. && make

# Comando para ejecutar la app (ajusta 'ProyectoPerro' al nombre de tu ejecutable)
CMD ["./build/ProyectoPerro"]