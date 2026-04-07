from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/raw/2025/voluntariado/cronograma_voluntariado_2025.xlsx")
OUTPUT_DIR = Path("data/processed/2025/voluntariado")
OUTPUT_FILE = OUTPUT_DIR / "BD_voluntariado_long.csv"

SHEET_NAME = "H4 Registro niños"


def cargar_archivo() -> pd.DataFrame:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {INPUT_FILE}")

    df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
    return df


def transformar() -> pd.DataFrame:
    bd = cargar_archivo()

    bd2 = bd.copy()

    # Cortar filas donde la segunda columna original esté vacía
    bd2 = bd2[bd2.iloc[:, 1].notna()].reset_index(drop=True)

    # Extraer filas clave del encabezado del archivo original
    actividad_row = bd.iloc[1]
    fecha_row = pd.to_datetime(bd.iloc[2], errors="coerce")
    fecha_str = fecha_row.dt.strftime("%Y-%m-%d")

    # Construir encabezados únicos: FECHA - ACTIVIDAD
    new_columns = []

    for col in range(bd.shape[1]):
        actividad = str(actividad_row[col]) if pd.notna(actividad_row[col]) else ""
        fecha = str(fecha_str[col]) if pd.notna(fecha_str[col]) else ""

        nombre_final = " - ".join([x for x in [fecha, actividad] if x]).strip(" -")
        new_columns.append(nombre_final)

    bd2.columns = new_columns

    # Eliminar filas usadas como encabezado
    bd2 = bd2.iloc[2:].reset_index(drop=True)

    # Eliminar primera columna (N°)
    bd2 = bd2.iloc[:, 1:]

    # Renombrar columnas fijas
    bd2.columns.values[0] = "DNI"
    bd2.columns.values[1] = "NOMBRES Y APELLIDOS"
    bd2.columns.values[2] = "GRADO"
    bd2.columns.values[3] = "SEXO"
    bd2.columns.values[4] = "CENTRO"
    bd2.columns.values[5] = "ESTADO"

    bd2.columns.values[-4] = "ASISTENCIAS PROGRAMADAS"
    bd2.columns.values[-3] = "ASISTENCIAS REALES"
    bd2.columns.values[-2] = "% PART."
    bd2.columns.values[-1] = "CONDICIÓN DE PARTICIPACIÓN"

    id_vars = [
        "DNI",
        "NOMBRES Y APELLIDOS",
        "GRADO",
        "SEXO",
        "CENTRO",
        "ESTADO",
        "ASISTENCIAS PROGRAMADAS",
        "ASISTENCIAS REALES",
        "% PART.",
        "CONDICIÓN DE PARTICIPACIÓN",
    ]

    activity_cols = [c for c in bd2.columns if str(c).startswith("2025-")]

    bd_long = bd2.melt(
        id_vars=id_vars,
        value_vars=activity_cols,
        var_name="FECHA_ACTIVIDAD",
        value_name="VALOR"
    )

    split_cols = bd_long["FECHA_ACTIVIDAD"].str.split(" - ", n=1, expand=True)

    if split_cols.shape[1] == 1:
        split_cols[1] = None

    bd_long["FECHA"] = pd.to_datetime(split_cols[0], errors="coerce")
    bd_long["ACTIVIDAD"] = split_cols[1]
    bd_long["MES"] = bd_long["FECHA"].dt.month_name()

    bd_long = bd_long.drop(columns=["FECHA_ACTIVIDAD"]).reset_index(drop=True)

    return bd_long


def main() -> None:
    print("=== TRANSFORMACIÓN VOLUNTARIADO ===")

    df_final = transformar()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("✅ Archivo generado")
    print(df_final.shape)
    print(OUTPUT_FILE.resolve())


if __name__ == "__main__":
    main()
