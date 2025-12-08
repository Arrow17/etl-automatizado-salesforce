
def renombrar_columnas_duplicadas(df):
    cols = df.columns
    nuevos = []
    contador = {}
    for c in cols:
        if c not in contador:
            contador[c] = 0
            nuevos.append(c)
        else:
            contador[c] += 1
            nuevos.append(f"{c}_v{contador[c]}")
    df = df.copy()
    df.columns = nuevos
    return df

def codebook(df, pk_col):
    resumen = pd.DataFrame({
        "Tipo": df.dtypes,
        "Nulos (#)": df.isnull().sum(),
        "Porcentaje Nulos (%)": df.isnull().mean() * 100,
        "Valores únicos (#)": df.nunique(),
    })
    resumen["Valores únicos (Muestra)"] = df.apply(
        lambda x: str(list(x.dropna().unique()[:5]))
    )
    return resumen.reset_index().rename(columns={"index": "Variable"})

def limpiar_y_generar_ficha_social_v2(file_path, output_folder):

    print(f"--- Procesando Ficha Social (v2) para: {file_path} ---")

    df = pd.read_excel(
        file_path,
        dtype={
            "Número de Documento": str,
            "Número de Documento.1": str,
            "Número de documento del niño": str
        }
    )

    df = renombrar_columnas_duplicadas(df)

    if "Marca temporal" in df.columns:
        df["Marca temporal"] = pd.to_datetime(df["Marca temporal"], errors="coerce")

    col_dni = "Número de documento del niño"
    df[col_dni] = df[col_dni].astype(str).str.replace(r"\.0$", "", regex=True)

    df = df.sort_values("Marca temporal", ascending=True)
    df = df.drop_duplicates(subset=[col_dni], keep="last")

    # garantizar strings
    for col in ["Número de Documento", "Número de Documento.1", col_dni]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    out_path = output_folder / "Ficha_Social_v2.xlsx"
    df_code = codebook(df, pk_col=col_dni)

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Ficha_Social_v2")
        df_code.to_excel(writer, index=False, sheet_name="Codebook")

    print(f"🎉 Archivo final generado: {out_path}")
