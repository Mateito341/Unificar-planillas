import pandas as pd
import glob
import os
from datetime import datetime

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
    
    dataframes_procesados = verificar(archivos)
    if dataframes_procesados:  # Solo continuar si hay DataFrames procesados
        subir(dataframes_procesados)



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
    Verifica los archivos y devuelve los DataFrames con columnas estandarizadas
    """
    dataframes_procesados = {}
    
    for archivo in archivos:
        try:
            df = pd.read_csv(archivo)
        except Exception as e:
            print(f"❌ Error al leer el archivo {archivo}: {e}")
            continue

        print(f"\n📄 Archivo leído: {archivo}")
        verificar_columnas(df)  # Esta función modifica el DataFrame directamente
        dataframes_procesados[archivo] = df
    
    return dataframes_procesados


def verificar_columnas(df):
    """
    Verifica que contenga las columnas esenciales, y si alguna tiene un nombre distinto,
    intenta detectarla y renombrarla. En caso de que no se encuentre, avisa al usuario.
    
    Args:
        df: archivo a verificar
    """

    columnas_originales = df.columns
    columnas_normalizadas = [c.strip().lower() for c in columnas_originales]
    mapeo_columnas = dict(zip(columnas_normalizadas, columnas_originales))

    for col in COLUMNAS_A_BUSCAR:
        col_lower = col.lower()
        if col_lower in columnas_normalizadas:
            # Renombrar siempre a la versión exacta de COLUMNAS_A_BUSCAR
            col_original = mapeo_columnas[col_lower]
            if col_original != col:  # Solo renombrar si es diferente
                df.rename(columns={col_original: col}, inplace=True)
            cantidad_nulls = df[col].isnull().sum()
            print(f"✅ '{col}' está presente. Valores nulos: {cantidad_nulls}")
            verificar_tipo_dato(df, col, col)
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
    Ademas verificar que la columna 'weed applied' sea del tipo correcto.
    
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

    elif col_normalizado == 'weed applied':
        valores_unicos = df[col_original].dropna().unique()
        for valor in valores_unicos:
            if valor not in [0, 1, '0', '1', None]:
                print(f"⚠️ Valor inesperado en 'weed applied': '{valor}'. Solo se permiten 0 y 1.")


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

    if col.lower() not in [k.lower() for k in equivalencias.keys()]:
        return None

    for posible in equivalencias[col]:
        posible_lower = posible.lower()
        if posible_lower in columnas_normalizadas:
            col_original = next((c for c in df.columns if c.strip().lower() == posible_lower), None)
            if col_original:
                cantidad_nulls = df[col_original].isnull().sum()
                df.rename(columns={col_original: col}, inplace=True)  # Renombrar al formato exacto
                return (col_original, cantidad_nulls)

    return None

def subir(dataframes_procesados):
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
        base_datos_subir(dataframes_procesados)
    else:
        print("No se subieron los datos a la base de datos.")

def base_datos_subir(dataframes_procesados):
    """
    Sube los datos a la base de datos finalmente.
    
    Args:
        archivos: archivos a subir
    """ 

    #funcion que crea los archivos standarizados, con la fecha, el nombre del cliente y quien lo subio
    archivos_estandarizados(dataframes_procesados)
    #funcion que los sube

def archivos_estandarizados(dataframes_procesados):
    """
    Crea los archivos estandarizados con sus respectivos datos, además de la fecha, 
    el nombre del cliente y quien lo subió (estos últimos dados por el usuario).
    Los guarda en la carpeta 'output_planillas'.
    
    El estándar incluye:
    - Columnas base: 'weed_count', 'date', 'client', 'user'
    - Columnas de datos: 'weed_diameter', 'size', 'height', 'weed_placement','weed_type', 'weed_name', 'weed_applied'
    
    Args:
        archivos: archivos a estandarizar
    """
    
    if not os.path.exists('output_planillas'):
        os.makedirs('output_planillas')
    
    for archivo, df in dataframes_procesados.items():
        print(f"\n📄 Procesando archivo: {archivo}")
        
        # Obtener metadatos
        while True:
            fecha = input("Ingrese la fecha del estudio (formato YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
                break
            except ValueError:
                print("Formato de fecha incorrecto. Use YYYY-MM-DD")
        
        cliente = input("Ingrese el nombre del cliente: ").strip()
        usuario = input("Ingrese su nombre: ").strip()
        
        # Crear DataFrame estandarizado
        df_estandar = pd.DataFrame()
        df_estandar['weed_count'] = range(1, len(df) + 1)
        df_estandar['date'] = fecha
        df_estandar['client'] = cliente
        df_estandar['user'] = usuario
        
        # Verificar columnas en el DataFrame ya procesado
        for col in COLUMNAS_A_BUSCAR:
            if col in df.columns:
                if col == "weed applied":
                    df_estandar[col] = df[col].apply(estandarizar_applied).astype("Int64")
                else:
                    df_estandar[col] = df[col]
            else:
                df_estandar[col] = pd.NA
                print(f"⚠️ Columna '{col}' no encontrada, se llenará con valores nulos")

        # Guardar archivo
        nombre_salida = f"estandarizado_{fecha}_{cliente}_{os.path.basename(archivo)}"
        ruta_salida = os.path.join('output_planillas', nombre_salida)
        df_estandar.to_csv(ruta_salida, index=False)
        print(f"✅ Archivo guardado: {ruta_salida}")

def estandarizar_applied(valor):
    """
    Estandariza valores para la columna 'weed applied':
    - Acepta: 1, 0, 1.0, 0.0, '1', '0', '1.0', '0.0', 'true', 'false'
    - Devuelve: 1 o 0 (int)
    - Si no es válido, devuelve pd.NA
    """
    if pd.isna(valor):
        return pd.NA

    if isinstance(valor, (int, float)):
        if valor == 1 or valor == 1.0:
            return 1
        elif valor == 0 or valor == 0.0:
            return 0
    elif isinstance(valor, str):
        valor_limpio = valor.strip().lower()
        if valor_limpio in ['1', '1.0', 'true']:
            return 1
        elif valor_limpio in ['0', '0.0', 'false']:
            return 0

    print(f"⚠️ Valor inválido en 'weed applied': '{valor}' → será reemplazado por vacío")
    return pd.NA

if __name__ == "__main__":
    main()
