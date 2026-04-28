# ETL Automatizado

Pipeline de datos para la extracción, transformación, validación y consolidación de registros provenientes de múltiples archivos Excel con estructuras heterogéneas.

---

## OBJETIVO

Automatizar completamente el procesamiento de para:

- Consolidar múltiples archivos Excel en un único dataset analítico
- Estandarizar estructuras inconsistentes entre centros y grados
- Transformar datos de formato ancho → largo
- Detectar y corregir errores de calidad de datos
- Generar outputs listos para consumo en Power BI / dashboards

---

## ARQUITECTURA DEL PIPELINE

Google Drive/Sharepoint → Extracción (Service Account) → data/raw → Transformación (Python - Pandas) → data/processed → CSV consolidado + reporte de calidad

---

## AUTOMATIZACIÓN (GITHUB ACTIONS)

El pipeline se ejecuta automáticamente mediante GitHub Actions con la siguiente configuración:

- Frecuencia: Lunes a Viernes
- Horarios: 08:00, 12:00, 16:00, 18:00


Los artefactos generados se eliminan automáticamente después de 1 día para evitar saturación de almacenamiento en GitHub.

---

## ESTRUCTURA DEL PROYECTO

```bash
.
├── data/
│   ├── raw/2025/
│   └── processed/2025/
│
├── scripts/
│   └── consolidacion_base.py
│
├── .github/workflows/
│   └── etl.yml
│
└── README.md
```

---

## PROBLEMAS RESUELTOS

Este pipeline está diseñado para resolver problemas comunes en archivos Excel reales:

- Encabezados en distintas filas → detección dinámica
- Columnas de fechas variables → identificación automática
- Datos en formato ancho → transformación a formato largo
- Estructuras inconsistentes entre grados → estandarización

---

## 🧪 VALIDACIONES EN LOGS

Durante la ejecución se generan logs clave para auditoría:

- Fila de encabezado detectada por hoja
- Columnas detectadas
- Índices de fechas
- Grados encontrados por hoja
- Filas eliminadas por falta de DNI
- Conteo final por grado

---

Un dataset limpio, consistente y listo para análisis, independientemente de las variaciones estructurales en los archivos fuente.
