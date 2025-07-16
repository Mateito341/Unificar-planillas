import pandas as pd
import glob
from sqlalchemy import create_engine

# Configuración de conexión (ajustá según tu caso)
db_url = "sqlite:///datos.db"  # Cambiá a tu conexión real
engine = create_engine(db_url)

# Columnas que queremos buscar
columnas_a_buscar = [
    "weed diameter",  # float
    "size",           # float
    "height",         # float
    "weed placement", # str
    "weed type",      # str
    "weed name",      # str
    "weed applied"    # bool
]

# Leer archivos
archivos = glob.glob("input_planillas/*.csv")
dfs_a_subir = []

for archivo in archivos:
    df = pd.read_csv(archivo)
    print(f"\n📄 Archivo leído: {archivo}")

    columnas_originales = df.columns
    columnas_normalizadas = [col.strip().lower() for col in columnas_originales]
    mapeo_columnas = dict(zip(columnas_normalizadas, columnas_originales))

    df_temp = pd.DataFrame()

    for col in columnas_a_buscar:
        if col in columnas_normalizadas:
            col_original = mapeo_columnas[col]
            nulos = df[col_original].isnull().sum()
            print(f"✅ '{col}' presente. Nulos: {nulos}")
            df_temp[col] = df[col_original]
        else:
            print(f"❌ '{col}' no está presente. Se rellenará con NaN.")
            df_temp[col] = pd.NA  # Completa con nulos

    # Agrega el archivo procesado a la lista
    dfs_a_subir.append(df_temp)

# Unimos todos los archivos
if dfs_a_subir:
    df_final = pd.concat(dfs_a_subir, ignore_index=True)

    print("\n¿Deseás subir los datos a la base incluso con columnas faltantes o nulos? (S/N)")
    respuesta = input().strip().upper()

    if respuesta == 'S':
        print("📤 Subiendo datos a la base...")
        df_final.to_sql("malezas", con=engine, if_exists="append", index=False)
        print("✅ Subida completada.")
    else:
        print("🚫 Subida cancelada por el usuario.")
else:
    print("⚠️ No se procesó ningún archivo.")
