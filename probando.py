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
    subir(archivos)


#FUNCIONES
def abrir_carpeta(carpeta):
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
        verificar_columnas(archivo)


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
    columnas_originales = df.columns
    columnas_normalizadas = [col.strip().lower() for col in columnas_originales]
    mapeo_columnas = dict(zip(columnas_normalizadas, columnas_originales))

    for col in COLUMNAS_A_BUSCAR:
        if col in columnas_normalizadas:
            col_original = mapeo_columnas[col]
            cantidad_nulls = df[col_original].isnull().sum()
            print(f"✅ '{col}' está presente. Valores nulos: {cantidad_nulls}")
            verificar_tipo_dato(col)
        else:
            # elif busqueda_profunda(col, columnas_normalizadas) else
            print(f"❌ '{col}' NO está presente.")

def verificar_tipo_dato(df, columna):
    """
    Verifica que los valores de una columna sean flotantes (para columnas numéricas).
    Para 'weed diameter', 'size' y 'height' debe ser float, de lo contrario muestra mensaje de error y lo especifica.
    
    Args:
        df: DataFrame de pandas
        columna: Nombre de la columna a verificar (en minúsculas y sin espacios extras)
    """
    # Columnas que deben ser flotantes
    columnas_flotantes = ['weed diameter', 'size', 'height']
    
    if columna in columnas_flotantes:
        # Obtener la columna original (puede tener mayúsculas o espacios diferentes)
        col_original = next((c for c in df.columns if c.strip().lower() == columna), None)      
            
        # Verificar cada valor no nulo
        for idx, valor in df[col_original].items():
            if pd.notna(valor):  # Solo verificar valores no nulos
                try:
                    float(valor)  # Intentar convertir a float
                except (ValueError, TypeError):
                    print(f"⚠️ Valor no flotante encontrado en '{col_original}', fila {idx}: '{valor}'")

def subir(archivos):
    """
    Le pregunta al usuario si a partir de la información ofrecida quiere subir los datos a
    la base de datos. En caso de que si lo sube, sino, termina el programa.
    
    Args:
        archivos: archivos a subir
    """
    
    print("\n¿Deseás subirlo a la base de datos? (S/N)")
    respuesta = input().strip().upper()

    if respuesta == 'S':
        print("Subiendo a la base de datos...")
        base_datos_subir(archivos)
    else:
        print("No se subieron los datos a la base de datos.")

def base_datos_subir(archivos):
    """
    Sube los datos a la base de datos finalmente.
    
    Args:
        archivos: archivos a subir
    """ 

    #crea los archivos standarizados
    #los junta
    #los sube

def busqueda_profunda(col, columnas_normalizadas, valores_nulos):
    """
    Se busca si la columna se registro con otro nombre, en caso de encontrarla avisarlo
    y decir porque nombre se cambio. Ejemplo:

    ✅🔄 'wide diameter' está presente (diametro -> 'weed diameter'). Valores nulos x
    
    Args:
        col: columna que deseamos encontrar
        columnas_normalizadas: todas las columnas
        valores_nulos: valores nulos
    """ 



if __name__ == "__main__":
    main()
