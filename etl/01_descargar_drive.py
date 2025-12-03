import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

print("=== Iniciando descarga desde Google Drive ===")

# 1. Leer JSON del Secret
service_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
if not service_json:
    raise ValueError("❌ No se encontró GOOGLE_SERVICE_ACCOUNT_JSON.")

# 2. Guardarlo como archivo temporal
with open("service_account.json", "w") as f:
    f.write(service_json)

# 3. Autenticación con Google API client
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = service_account.Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=creds)

print("✔ Autenticación correcta")

# 4. ID del archivo Google Sheets
FILE_ID = "1jx7eXk_lPHiNGrmLwkWmd8-4wEVTkPeZ"

# 5. Crear carpeta /data
os.makedirs("data", exist_ok=True)
output_path = "data/Ficha_Social_respuestas.xlsx"

print("⬇ Exportando Google Sheets a Excel (.xlsx)...")

# 6. Descargar archivo convertido
request = drive_service.files().export_media(
    fileId=FILE_ID,
    mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Guardar archivo
with open(output_path, "wb") as fh:
    downloader = request.execute()
    fh.write(downloader)

print(f"🎉 Descarga completada: {output_path}")

