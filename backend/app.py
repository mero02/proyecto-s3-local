from flask import Flask, request, jsonify, render_template
import boto3
from botocore.exceptions import ClientError
import os

# Inicializamos la aplicación Flask
app = Flask(__name__)

# ---------------------------------------
# Configuración para usar S3 en LocalStack
# ---------------------------------------

# URL del servicio de LocalStack
LOCALSTACK_ENDPOINT = os.getenv('LOCALSTACK_ENDPOINT', 'http://localhost:4566')

# Nombre del bucket donde guardaremos archivos
BUCKET_NAME = 'mi-bucket-local'

# Cliente S3 configurado para apuntar a LocalStack
s3_client = boto3.client(
    's3',
    endpoint_url=LOCALSTACK_ENDPOINT,  # Se conecta a LocalStack y no a AWS real
    aws_access_key_id='test',          # LocalStack acepta cualquier credencial
    aws_secret_access_key='test',
    region_name='us-east-1'            # Región estándar
)

# ------------------------------------------------
# Función para crear el bucket si no existe aún
# ------------------------------------------------
def create_bucket_if_not_exists():
    try:
        # Verifica si el bucket existe
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except ClientError as e:
        # Si no existe lo creamos
        if e.response['Error']['Code'] == '404':
            s3_client.create_bucket(Bucket=BUCKET_NAME)
        else:
            raise

# -------------------------------
# Ruta principal (frontend HTML)
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html') # Renderizamos al index

# ---------------------------------------
# Ruta para subir archivos al bucket S3
# ---------------------------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica que la clave 'file' exista en el formulario
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Si no se seleccionó ningún archivo
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Aseguramos que el bucket exista
        create_bucket_if_not_exists()

        # Subimos el archivo a S3 (LocalStack)
        s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)

        return jsonify({'message': f'File {file.filename} uploaded successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------------------
# Ruta para listar archivos dentro del bucket
# -----------------------------------------
@app.route('/files', methods=['GET'])
def list_files():
    try:
        # Aseguramos que el bucket exista
        create_bucket_if_not_exists()

        # Pedimos la lista de objetos almacenados
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)

        files = []

        # Si el bucket tiene archivos, estarán en 'Contents'
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat()
                })

        return jsonify(files), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ----------------------------------------
# Ejecución de la aplicación Flask
# ----------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
