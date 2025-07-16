import pandas as pd
import glob

# Columnas que queremos verificar
COLUMNAS_A_BUSCAR = [
    "weed diameter",  # diametro (float)
    "size",           # tamaño cm2 (float)
    "height",         # altura (float)
    "weed placement", # lugar (string)
    "weed type",      # tipo (string)
    "weed name",      # nombre (string)
    "weed applied"    # aplicado (bool)
]

def main():

    archivos = abrir_carpeta("input_planillas")

    if not archivos:
        return
    
    verificar(archivos)
    #subir(archivos)


#FUNCIONES
def abrir_carpeta(carpeta): #hecho
    """
    Abre la carpeta que contiene la planilla de los distintos clientes en formato (.csv).
    
    Args:
        carpeta: carpeta donde se encuentran los archivos
    """
    archivos = glob.glob(f"{carpeta}/*.csv")

    if not archivos:
        print(f"⚠️ No se encontraron archivos en la carpeta '{carpeta}/'.")
        return []

    return archivos


def verificar(archivos):
    """
    Verifica que los archivos este en condiciones para poder subirse. 
    Advierte al usuario de los posibles errores que pueden suceder.
    
    Args:
        archivos: todos los archivos a verificar
    """

    for archivo in archivos:
        try:
            df = pd.read_csv(archivo)
        except Exception as e:
            print(f"❌ Error al leer el archivo {archivo}: {e}")
            return

        print(f"\n📄 Archivo leído: {archivo}")
        verificar_columnas(df)


def verificar_columnas(df):
    """
    Verifica que contenga las columnas esenciales, es decir las que a nosotros nos importa. Como pueden ser:
    "size",           # tamaño cm2 (float)
    "height",         # altura (float)
    "weed placement", # lugar (string)
    "weed type",      # tipo (string)
    "weed name",      # nombre (string)
    "weed applied"    # aplicado (bool)
    En caso de que no esten advertir que no se encontro.
    
    Args:
        df: arhivo a verificar
    """

    # Normalizar nombres de columnas
    columnas_originales = df.columns # guarda todos los nombres de la columnas
    columnas_normalizadas = [col.strip().lower() for col in columnas_originales] # guarda todos los nombres de la columnas en minusculas y sin espacios extras

    for col in COLUMNAS_A_BUSCAR:
        if col in columnas_normalizadas:
            cantidad_nulls = df[col].isnull().sum()
            print(f"✅ '{col}' está presente. Valores nulos: {cantidad_nulls}")
            #verificar_tipo_dato(col)
        else:
            # elif busqueda_profunda(col, columnas_normalizadas) else
            print(f"❌ '{col}' NO está presente.")


if __name__ == "__main__":
    main()
