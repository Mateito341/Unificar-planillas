import streamlit as st
import pandas as pd
import datetime
from pymongo import MongoClient

# Conexión a MongoDB local
client = MongoClient("mongodb://localhost:27017")
db = client["ensayos_db"]
coleccion = db["formularios"]

st.set_page_config(page_title="Formulario de Ensayos", layout="wide")
st.title("Formulario de Ensayos")

tabs = st.tabs([
    "🧑‍🌾 Información del Ensayo",
    "🌍 Condiciones del Lote",
    "📋 Detalles de Aplicación",
    "🛠️ Evaluación",
    "📤 Enviar"
])

# RECOLECTAMOS LOS DATOS FUERA DE CUALQUIER FORMULARIO
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧾 Cliente")
        name = st.text_input("Nombre del cliente")
        sprai_id = st.text_input("ID del sistema pulverizador")
        modules_id = st.text_input("ID de los módulos utilizados")
        st.subheader("👷 Personal")
        machine_operator = st.text_input("Operador de la máquina")
        trial_testers = st.text_input("Evaluadores del ensayo")
    with col2:
        st.subheader("🗓️ Datos del ensayo")
        test_date = st.date_input("Fecha del ensayo", value=datetime.date.today())
        test_time = st.time_input("Hora del ensayo")

with tabs[1]:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📍 Ubicación")
        farm = st.text_input("Nombre de la finca")
        farm_address = st.text_input("Dirección de la finca")
        field_location = st.text_input("Ubicación del lote")
        latitude = st.text_input("Latitud")
        longitude = st.text_input("Longitud")
        soil_type = st.text_input("Tipo de suelo")
    with col2:
        st.subheader("🌦️ Condiciones Ambientales")
        ambient_temperature = st.number_input("Temperatura ambiente (°C)")
        wind_speed = st.number_input("Velocidad del viento (km/h)")
        relative_humidity = st.number_input("Humedad relativa (%)")
        wind_direction = st.text_input("Dirección del viento")
        ambient_light_intensity = st.number_input("Intensidad de luz")
    with col3:
        st.subheader("🌱 Cultivo")
        crop_specie = st.text_input("Especie del cultivo")
        tillage = st.selectbox("¿Suelo labrado?", ["Sí", "No"])
        row_spacing = st.number_input("Distancia entre hileras(cm)")
        crop_population = st.number_input("Población por hectárea")
        crop_stage = st.text_input("Estado fenológico")

with tabs[2]:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🚜 Pulverizadora")
        sprayer_manufacturer = st.text_input("Fabricante")
        sprayer_model_number = st.text_input("Modelo")
        sprayer_year = st.text_input("Año de fabricación")
        nozzle_nomenclature = st.text_input("Nomenclatura de boquillas")
        nozzle_droplet_classification = st.text_input("Clasificación de gotas")
        nozzle_spacing = st.number_input("Espaciado de boquillas (cm)")
        boom_height = st.number_input("Altura del botalón (cm)")
        speed = st.number_input("Velocidad (km/h)")
        spray_pressure = st.number_input("Presión de aplicación (bar)")
        flow_rate = st.number_input("Caudal (L/min)")
    with col2:
        st.subheader("🧪 Colorante")
        dye_used = st.text_input("Tipo de colorante")
        dye_manufacturer = st.text_input("Fabricante", key="dye_manufacturer")
        dye_concentration = st.number_input("Concentración (%)")
        sensitivity = st.number_input("Sensibilidad")
        tile_size = st.number_input("Tamaño (μm)")
    with col3:
        st.subheader("💧 Herbicida")
        herbicide = st.text_input("Nombre del herbicida")
        dose = st.text_input("Dosis aplicada")

with tabs[3]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌾 Modelo de Detección")
        sens = st.selectbox("Sensibilidad", [1, 2, 3])
        tile = st.selectbox("Baldosa", [1, 2, 3])
    with col2:
        st.subheader("📊 Resultados Malezas")
        st.write("Subí un archivo CSV con los datos de malezas")
        csv_file = st.file_uploader("Cargar archivo CSV", type=["csv"])
        uploader = st.text_input("Persona que cargó los datos")

with tabs[4]:
    st.subheader("Resumen")

    st.markdown("#### 🧑‍🌾 Información del Ensayo")
    st.write("**🧾 Cliente**")
    st.write(f"- Nombre: {name}")
    st.write(f"- ID Pulverizador: {sprai_id}")
    st.write(f"- ID Modulos: {modules_id}")
    st.write("**👷 Personal**")
    st.write(f"- Operador: {machine_operator}")
    st.write(f"- Evaluadores: {trial_testers}")
    st.write("**🗓️ Datos del ensayo**")
    st.write(f"- Fecha: {test_date}")
    st.write(f"- Hora: {test_time}")

    st.markdown("#### 🌍 Condiciones del Lote")
    st.write("**📍 Ubicación**")
    st.write(f"- Finca: {farm}")
    st.write(f"- Dirección: {farm_address}")
    st.write(f"- Ubicación: {field_location}")
    st.write(f"- Latitud: {latitude}")
    st.write(f"- Longitud: {longitude}")
    st.write(f"- Tipo de Suelo: {soil_type}")
    st.write("**🌦️ Condiciones Ambientales**")
    st.write(f"- Temperatura: {ambient_temperature} °C")
    st.write(f"- Velocidad del viento: {wind_speed} km/h")
    st.write(f"- Humedad relativa: {relative_humidity} %")
    st.write(f"- Dirección del viento: {wind_direction}")
    st.write(f"- Intensidad de luz: {ambient_light_intensity}")
    st.write("**🌱 Cultivo**")
    st.write(f"- Cultivo: {crop_specie}")
    st.write(f"- Suelo labrado: {tillage}")
    st.write(f"- Distancia entre hileras: {row_spacing} cm")
    st.write(f"- Población por hectárea: {crop_population}")
    st.write(f"- Estado fenológico: {crop_stage}")

    st.markdown("#### 📋 Detalles de Aplicación")
    st.write("**🚜 Pulverizadora**")
    st.write(f"- Fabricante: {sprayer_manufacturer}")
    st.write(f"- Modelo: {sprayer_model_number}")
    st.write(f"- Año: {sprayer_year}")
    st.write(f"- Nomenclatura de boquillas: {nozzle_nomenclature}")
    st.write(f"- Clasificación de gotas: {nozzle_droplet_classification}")
    st.write(f"- Espaciado de boquillas: {nozzle_spacing} cm")
    st.write(f"- Altura del botalón: {boom_height} cm")
    st.write(f"- Velocidad: {speed} km/h")
    st.write(f"- Presión de aplicación: {spray_pressure} bar")
    st.write(f"- Caudal: {flow_rate} L/min")
    st.write("**🧪 Colorante**")
    st.write(f"- Tipo: {dye_used}")
    st.write(f"- Fabricante: {dye_manufacturer}")
    st.write(f"- Concentración: {dye_concentration} %")
    st.write(f"- Sensibilidad: {sensitivity}")
    st.write(f"- Tamaño: {tile_size} μm")
    st.write("**💧 Herbicida**")
    st.write(f"- Nombre: {herbicide}")
    st.write(f"- Dosis: {dose}")

    st.markdown("#### 🛠️ Evaluación")
    st.write("**🌾 Modelo de Detección**")
    st.write(f"- Sensibilidad: {sens}")
    st.write(f"- Baldosa: {tile}")
    if csv_file:
        st.write("- Archivo CSV cargado correctamente")

    st.subheader("Confirmar envío")

    # Solo el botón y el envío están en el formulario
    with st.form("form_envio"):
        submit = st.form_submit_button("Enviar Formulario Completo")

if submit:
    # Prepare the form data as a dictionary
    form_data = {
        # Tab 1: Información del Ensayo
        "cliente": {
            "nombre": name,
            "sprai_id": sprai_id,
            "modules_id": modules_id
        },
        "personal": {
            "operador": machine_operator,
            "evaluadores": trial_testers
        },
        "datos_ensayo": {
            "fecha": test_date.isoformat(),
            "hora": str(test_time)
        },
        
        # Tab 2: Condiciones del Lote
        "ubicacion": {
            "finca": farm,
            "direccion": farm_address,
            "lote": field_location,
            "latitud": latitude,
            "longitud": longitude,
            "tipo_suelo": soil_type
        },
        "condiciones_ambientales": {
            "temperatura": ambient_temperature,
            "velocidad_viento": wind_speed,
            "humedad": relative_humidity,
            "direccion_viento": wind_direction,
            "intensidad_luz": ambient_light_intensity
        },
        "cultivo": {
            "especie": crop_specie,
            "suelo_labrado": tillage,
            "distancia_hileras": row_spacing,
            "poblacion_hectarea": crop_population,
            "estado_fenologico": crop_stage
        },
        
        # Tab 3: Detalles de Aplicación
        "pulverizadora": {
            "fabricante": sprayer_manufacturer,
            "modelo": sprayer_model_number,
            "año": sprayer_year,
            "boquillas": {
                "nomenclatura": nozzle_nomenclature,
                "clasificacion_gotas": nozzle_droplet_classification,
                "espaciado": nozzle_spacing
            },
            "configuracion": {
                "altura_botalon": boom_height,
                "velocidad": speed,
                "presion": spray_pressure,
                "caudal": flow_rate
            }
        },
        "colorante": {
            "tipo": dye_used,
            "fabricante": dye_manufacturer,
            "concentracion": dye_concentration,
            "sensibilidad": sensitivity,
            "tamaño": tile_size
        },
        "herbicida": {
            "nombre": herbicide,
            "dosis": dose
        },
        
        # Tab 4: Evaluación
        "evaluacion": {
            "modelo_deteccion": {
                "sensibilidad": sens,
                "baldosa": tile
            },
            "archivo_csv": "subido" if csv_file else "no_subido",
            "persona_carga": uploader
        },
        
        # Metadata
        "fecha_creacion": datetime.datetime.now().isoformat(),
        "estado": "completado"
    }
    
    # Handle CSV file if uploaded
    if csv_file:
        try:
            # Read CSV file
            csv_data = pd.read_csv(csv_file)
            # Convert to dictionary and add to form_data
            form_data["evaluacion"]["datos_csv"] = csv_data.to_dict(orient="records")
        except Exception as e:
            st.warning(f"Advertencia: No se pudo procesar el archivo CSV. Error: {str(e)}")
    
    try:
        # Insert into MongoDB
        coleccion.insert_one(form_data)
        st.success("✅ Formulario enviado correctamente a la base de datos")
        st.balloons()
        st.subheader("📋 Resumen Completo")
        st.json(form_data, expanded=False)
    except Exception as e:
        st.error(f"Error al enviar el formulario: {str(e)}")
