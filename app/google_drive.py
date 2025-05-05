from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import os

# Si modificas el alcance, borra el token.json
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_drive(file_path, file_name=None):
    creds = None

    # Carga credenciales si ya están guardadas
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Si no hay credenciales válidas, pide autorización
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Guarda las credenciales para la próxima vez
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Conectar con la API de Google Drive
    service = build('drive', 'v3', credentials=creds)

    # Configurar el archivo a subir
    file_metadata = {'name': file_name or os.path.basename(file_path)}
    media = MediaFileUpload(file_path, resumable=True)

    # Subir el archivo
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Archivo subido correctamente. ID: {file.get('id')}")
