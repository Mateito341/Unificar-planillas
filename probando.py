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


#FUNCIONES VERIFICAR
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
    Verifica que contenga las columnas esenciales, y si alguna tiene un nombre distinto,
    intenta detectarla y renombrarla.
    
    Args:
        df: archivo a verificar
    """

    for col in COLUMNAS_A_BUSCAR:
        # Normalizamos los nombres actualizados en cada iteración
        columnas_originales = df.columns
        columnas_normalizadas = [c.strip().lower() for c in columnas_originales]
        mapeo_columnas = dict(zip(columnas_normalizadas, columnas_originales))

        if col in columnas_normalizadas:
            col_original = mapeo_columnas[col]
            cantidad_nulls = df[col_original].isnull().sum()
            print(f"✅ '{col}' está presente. Valores nulos: {cantidad_nulls}")
            verificar_tipo_dato(df, col_original, col)
        else:
            resultado = busqueda_profunda(col, columnas_normalizadas, df)
            if resultado:
                col_encontrada, nulos = resultado
                print(f"✅🔄 '{col}' fue encontrado como '{col_encontrada}' y renombrado. Valores nulos: {nulos}")
                verificar_tipo_dato(df, col, col)
            else:
                print(f"❌ '{col}' NO está presente.")


def verificar_tipo_dato(df, col_original, col_normalizado):
    """
    Verifica que los valores de una columna sean del tipo esperado.
    
    Para columnas numéricas ('weed diameter', 'size', 'height') debe ser float.
    
    Args:
        df: DataFrame
        col_original: nombre original (como está en el archivo)
        col_normalizado: nombre limpio (minúscula y sin espacios)
    """
    columnas_flotantes = ['weed diameter', 'size', 'height']

    if col_normalizado in columnas_flotantes:
        for idx, valor in df[col_original].items():
            if pd.notna(valor):
                try:
                    float(valor)
                except (ValueError, TypeError):
                    print(f"⚠️ Valor no flotante en '{col_original}' (fila {idx}): '{valor}'")

#FUNCIONES SUBIR
def busqueda_profunda(col, columnas_normalizadas, df):
    """
    Busca columnas equivalentes (en otro idioma o sinónimos) y si las encuentra,
    renombra la columna del DataFrame para que se llame como `col`.

    Args:
        col: nombre estándar buscado (normalizado)
        columnas_normalizadas: lista de columnas normalizadas (minúsculas, sin espacios)
        df: DataFrame actual

    Returns:
        tuple: (nuevo_nombre (col), cantidad_nulls) si se renombró, None si no se encontró
    """
    equivalencias = {
        'weed diameter': ['diametro', 'diameter', 'diametro maleza'],
        'size': ['tamaño', 'area', 'superficie'],
        'height': ['altura', 'alto'],
        'weed placement': ['lugar', 'ubicacion', 'posicion', 'localizacion'],
        'weed type': ['tipo', 'tipo maleza', 'clase', 'categoria'],
        'weed name': ['nombre', 'identificacion', 'nombre maleza'],
        'weed applied': ['aplicado', 'se aplicó', 'fue aplicado']
    }


    if col not in equivalencias:
        return None

    for posible in equivalencias[col]:
        if posible == col:
            continue  # Evitar "sinónimo" igual al nombre estándar

        if posible in columnas_normalizadas:
            col_original = next((c for c in df.columns if c.strip().lower() == posible), None)
            if col_original:
                cantidad_nulls = df[col_original].isnull().sum()
                df.rename(columns={col_original: col}, inplace=True)
                return (col_original, cantidad_nulls)

    return None

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


if __name__ == "__main__":
    main()
