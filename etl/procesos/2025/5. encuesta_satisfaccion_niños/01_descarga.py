import os
import requests

print("=== Descargando Google Sheets como Excel ===")

# ID del archivo
FILE_ID = "1ELmiuXjpfw644mck9pMLMROHeEBE1E29"

# Ruta correcta (ALINEADA)
OUTPUT_PATH = "data/raw/2025/5.encuesta_satisfaccion_ninos/Encuesta_Satisfaccion_Ninos.xlsx"

# URL export
export_url = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=xlsx"

# Autenticación
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
SERVICE_ACCOUNT_JSON = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]

creds = Credentials.from_service_account_info(
    eval(SERVICE_ACCOUNT_JSON),
    scopes=SCOPES
)

authed = AuthorizedSession(creds)

print("✓ Autenticación correcta")

# Descargar archivo
response = authed.get(export_url)

if response.status_code != 200:
    print("Error en descarga:", response.text)
    raise SystemExit(1)

# Crear carpeta correctamente
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, "wb") as f:
    f.write(response.content)

print(f"✓ Archivo descargado correctamente → {OUTPUT_PATH}")
