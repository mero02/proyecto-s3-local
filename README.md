# Proyecto S3 Local

## Descripción
Este proyecto simula un servicio de almacenamiento Amazon S3 localmente utilizando LocalStack. Está diseñado para el Laboratorio 3 de Sistemas Distribuidos, permitiendo subir y listar archivos en un bucket simulado sin necesidad de AWS real.

## Tecnologías
- **Backend**: Python 3.9, Flask, boto3
- **Frontend**: HTML5, CSS3, JavaScript
- **Contenedorización**: Docker, Docker Compose
- **Simulación S3**: LocalStack con gresau/localstack-persist

## Estructura del Proyecto
- `backend/`: Código del servidor Flask
- `frontend/`: Interfaz web
- `docker-compose.yml`: Configuración de servicios
- `Dockerfile`: Construcción de la imagen de la app

## Requisitos
- Docker
- Docker Compose

## Instalación y Ejecución
1. Clona el repositorio `git clone git@github.com:mero02/proyecto-s3-local.git`
2. Navega al directorio del proyecto.
3. Ejecuta `docker-compose up --build` para construir y levantar los servicios.
4. Accede a http://localhost:5000 en tu navegador.

## Uso
- Sube archivos utilizando el formulario en la página principal.
- Lista los archivos subidos en la tabla, con paginación.
- Los datos se persisten en los directorios `localstack-data` y `localstack-s3-data` usando gresau/localstack-persist.

## Funcionalidades
- Subida de archivos al bucket S3 simulado.
- Listado paginado de archivos.
- Interfaz web responsiva.

## Notas
- LocalStack simula S3 localmente para desarrollo usando gresau/localstack-persist.
- El bucket se crea automáticamente si no existe.
- **Persistencia**: Los datos persisten durante reinicios de contenedores, pero no entre sesiones completas de Docker. Para persistencia permanente, considerar LocalStack Pro.