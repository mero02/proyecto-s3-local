# Simulación de Amazon S3 Local con LocalStack y Flask

## Resumen Ejecutivo

Este proyecto implementa un servicio local que simula Amazon S3 utilizando LocalStack dentro de Docker, con un servidor web en Flask que permite subir archivos y listar los contenidos de un bucket S3 local. La solución proporciona una alternativa económica para desarrollo y testing sin incurrir en costos de AWS.

## Mejoras Implementadas

- **Contenerización Completa:** Tanto el backend como el frontend están contenerizados, permitiendo despliegue con un solo comando `docker-compose up -d`.
- **Layout Mejorado:** Interfaz de dos columnas (subida izquierda, lista derecha).
- **Paginación:** Lista de archivos paginada para manejar grandes cantidades de archivos eficientemente.
- **Persistencia Limitada:** Los datos no persisten entre reinicios completos de contenedores (limitación de LocalStack gratuita).

## Tecnologías Utilizadas

### Docker
**Definición:** Plataforma de contenedorización que permite empaquetar aplicaciones y sus dependencias en contenedores aislados, garantizando consistencia entre diferentes entornos.

### Dockerfile
**Definición:** Archivo de texto que contiene instrucciones para construir una imagen Docker. Define el entorno de ejecución de la aplicación, incluyendo el sistema operativo base, dependencias y comandos de inicio.

### LocalStack
**Definición:** Herramienta que emula servicios de AWS localmente, permitiendo desarrollar y probar aplicaciones cloud sin conectarse a la nube real.

### Python
**Definición:** Lenguaje de programación interpretado de alto nivel, conocido por su sintaxis clara y versatilidad, utilizado aquí para la lógica del servidor.

### Flask
**Definición:** Framework web minimalista escrito en Python que facilita la creación de aplicaciones web y APIs con herramientas y bibliotecas esenciales.

### Boto3
**Definición:** SDK oficial de AWS para Python que permite interactuar programáticamente con servicios de AWS, configurado aquí para apuntar a LocalStack.

### AWS S3
**Definición:** Servicio de almacenamiento de objetos de Amazon Web Services que ofrece escalabilidad, disponibilidad y seguridad para datos.

### Contenerización
**Definición:** Técnica para empaquetar aplicaciones y sus dependencias en contenedores aislados, facilitando despliegue y escalabilidad.

---
---
## Pruebas de Persistencia Realizadas

Durante el desarrollo del proyecto, realizamos pruebas exhaustivas para verificar la persistencia de datos en LocalStack.

### Fase 1: Configuración Inicial de Persistencia
- Implementamos volúmenes bind mount en `docker-compose.yml` para montar `./localstack-data` en `/opt/localstack/data`.
- Configuramos las variables de entorno `PERSISTENCE=1` y `DATA_DIR=/opt/localstack/data`.
- Levantamos los servicios y subimos archivos de prueba para verificar funcionamiento básico.

### Fase 2: Pruebas de Reinicio Básico
- Reiniciamos los contenedores con `docker-compose restart`.
- Verificamos que los archivos subidos seguían accesibles vía la API.
- Resultado: Los archivos persistían durante la sesión, pero se perdían al detener completamente los contenedores.

### Fase 3: Investigación de Almacenamiento Interno
- Inspeccionamos el sistema de archivos del contenedor LocalStack.
- Descubrimos que los archivos S3 se almacenan en `/tmp/localstack-s3-storage/bucket/key`.
- Intentamos montar este directorio con volúmenes adicionales (`./localstack-s3-data:/tmp/localstack-s3-storage`).
- Resultado: El bucket se creaba en el host, pero los archivos no se guardaban físicamente.

### Fase 4: Implementación de Base de Datos Externa
- Agreguamos PostgreSQL como servicio en `docker-compose.yml`.
- Configuramos `PERSISTENCE_DB_URL` para que LocalStack use la DB externa.
- Levantamos los servicios con la nueva configuración.
- Verificamos si se creaban tablas en PostgreSQL.
- Resultado: PostgreSQL funcionaba, pero LocalStack no utilizaba la DB; no se crearon tablas ni se guardaron datos.

### Resultados Finales de las Pruebas
- **Subida de Archivos**: Funciona correctamente durante la sesión activa.
- **Persistencia de Metadatos**: No se mantiene entre reinicios completos.
- **Persistencia de Archivos**: Los archivos no sobreviven a `docker-compose down`.
- **Base de Datos**: No se utiliza por LocalStack en esta configuración.

### Conclusión
LocalStack versión 3.0 gratuita tiene limitaciones importantes en persistencia. Para un laboratorio académico como este, es suficiente para testing en sesiones activas, pero no garantiza persistencia permanente. Para producción o persistencia real, recomendaría LocalStack Pro.

---



## Guía Paso a Paso

### Prerrequisitos
- Docker y Docker Compose instalados
- Git (opcional)

### Paso 1: Configuración del Entorno

1. **Clonar/Descargar el proyecto:**
   ```bash
   # Si está en un repositorio git
   git clone git@github.com:mero02/proyecto-s3-local.git
   cd proyecto
    ```
2. **Verificar estructura de archivos:**
Asegúrate de tener los siguientes archivos:

 - docker-compose.yml
 - app.py
 - requirements.txt
 - templates/index.html
 - static/style.css

### Paso 2: Ejecutar Todos los Servicios con Docker Compose
1. **Levantar los servicios:**
    ```bash
    docker-compose up -d
    ```

2. **Verificar que los servicios estén ejecutándose:**
    ```bash
    docker-compose ps
    ```
  - Deberías ver los contenedores `app` y `localstack` en estado "Up".
### Paso 3: Usar la Aplicación Web
1. **Acceder a la aplicación:**
 - Abre tu navegador y ve a:
    ```bash
    http://localhost:5000
    ```
2. **Interfaz principal:**
 - Verás un formulario para subir archivos
 - Una lista de archivos ya cargados (inicialmente vacía)

3. **Subir un archivo:**
 - Haz clic en "Seleccionar archivo"
 - Elige cualquier archivo de tu computadora
 - Haz clic en "Subir archivo"
 - Verás un mensaje de confirmación
 4. **Ver resultados:**
 - El archivo aparecerá en la lista debajo del formulario
 - Puedes subir múltiples archivos

### Paso 4: Donde Ver los Resultados
1. **En la Aplicación Web**
 - Lista de archivos: En la sección "Archivos en el Bucket" de la página principal
 - Confirmaciones: Mensajes de éxito/error después de cada operación

2. **En los Logs**
 - Logs de Docker/LocalStack:
    ```bash
    docker-compose logs localstack
    ```
3. **Logs de Flask:**
  - Logs del contenedor de la app:
    ```bash
    docker-compose logs app
    ```

4. **En el Sistema de Archivos de LocalStack**
 - Los archivos se almacenan en el volumen de Docker. Para inspeccionar:
    ```bash
    # 1. Acceder al contenedor de LocalStack
    docker exec -it sd2025-lab3-p3-localstack-1 bash

    # 2. Configurar credenciales AWS dummy (solo primera vez)
    aws configure set aws_access_key_id test
    aws configure set aws_secret_access_key test
    aws configure set default.region us-east-1

    # 3. Listar archivos en el bucket via AWS CLI
    aws --endpoint-url=http://localhost:4566 s3 ls s3://mi-bucket-local/

    # 4. También puedes navegar al directorio físico
    cd /tmp/localstack-s3-storage/mi-bucket-local/
    ls -la

    # 5. Para ver detalles de un archivo específico
    aws --endpoint-url=http://localhost:4566 s3api head-object --bucket mi-bucket-local --key TL3.pdf

    # 6. Descargar un archivo (se guarda DENTRO del contenedor)
    aws --endpoint-url=http://localhost:4566 s3 cp s3://mi-bucket-local/TL3.pdf /tmp/verificacion.pdf
    # El archivo se guarda en: /tmp/verificacion.pdf (DENTRO del contenedor)

    # 7. Para SALIR del contenedor cuando termines
    exit

5. **Desde la maquina local (Host)**
    ```bash
    # 1. Listar archivos (sin entrar al contenedor)
    docker exec sd2025-lab3-p3-localstack-1 aws --endpoint-url=http://localhost:4566 s3 ls s3://mi-bucket-local/

    # 2. Descargar archivo directamente a tu PC
    docker exec sd2025-lab3-p3-localstack-1 aws --endpoint-url=http://localhost:4566 s3 cp s3://mi-bucket-local/TL3.pdf /tmp/descarga.pdf
    docker cp sd2025-lab3-p3-localstack-1:/tmp/descarga.pdf ~/Escritorio/TL3-descargado.pdf
    # El archivo se guarda en: ~/Escritorio/TL3-descargado.pdf (en tu PC)

6. **Comandos útiles adicionales**
    ```bash
    # Ver todos los buckets existentes
    docker exec sd2025-lab3-p3-localstack-1 aws --endpoint-url=http://localhost:4566 s3 ls

    # Ver información detallada del bucket
    docker exec sd2025-lab3-p3-localstack-1 aws --endpoint-url=http://localhost:4566 s3api list-objects --bucket mi-bucket-local

    # Eliminar un archivo (si necesitas limpiar)
    docker exec sd2025-lab3-p3-localstack-1 aws --endpoint-url=http://localhost:4566 s3 rm s3://mi-bucket-local/TL3.pdf

### Paso 5: Detener los Servicios
1. **Detener todos los servicios:**
     ```bash
     docker-compose down
     ```
2. **Detener y eliminar volúmenes (para limpiar datos persistentes):**
     ```bash
     docker-compose down -v
     ```
3. **Estructura del Proyecto**
     ```bash
     proyecto/
     ├── backend/
     │   ├── app.py               # Aplicación Flask principal
     │   └── requirements.txt     # Dependencias de Python
     ├── frontend/
     │   ├── templates/
     │   │   └── index.html      # Interfaz web
     │   └── static/
     │       └── style.css       # Estilos CSS
     ├── docker-compose.yml       # Configuración de servicios Docker
     ├── Dockerfile               # Imagen para la aplicación completa
     ├── localstack-data/         # Datos persistentes de LocalStack
     ├── Informe.md               # Esta documentación
     └── README.md                # Documentacion basica
     ```

4. **Comandos Útiles para Debugging**
    ```bash
    # Ver estado de contenedores
    docker-compose ps

    # Ver logs en tiempo real
    docker-compose logs -f localstack

    # Ver información del bucket desde CLI
    docker exec sd2025-lab3-p3-localstack-1 aws --endpoint-url=http://localhost:4566 s3 ls s3://mi-bucket-local/

    # Limpiar todo
    docker-compose down -v
    ```
## Conclusión
Esta implementación proporciona un entorno completo de desarrollo local para trabajar con S3, ideal para testing y desarrollo sin costos de cloud. La combinación de Docker, LocalStack y Flask crea un ecosistema robusto y aislado para el manejo de archivos.