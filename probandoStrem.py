import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Formulario de Ensayos", layout="wide")
st.title("Formulario de Ensayos")

# Crear los 5 tabs según especificación
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧾 Cliente & Ensayo", 
    "📍 Ubicación & Ambiente", 
    "🌱 Cultivo & Pulverizadora", 
    "💧 Colorante, Herbicida & Personal", 
    "🌾 Modelo & Resultados"
])

# TAB 1: Cliente + Ensayo
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🧾 Cliente")
        with st.form("form_cliente"):
            name = st.text_input("Nombre del cliente")
            sprai_id = st.text_input("ID del sistema pulverizador")
            modules_id = st.text_input("ID de los módulos utilizados")
            submitted_cliente = st.form_submit_button("Guardar Cliente")
    
    with col2:
        st.header("🗓️ Datos del ensayo")
        with st.form("form_ensayo"):
            test_date = st.date_input("Fecha del ensayo", value=datetime.date.today())
            test_time = st.time_input("Hora del ensayo")
            submitted_ensayo = st.form_submit_button("Guardar Ensayo")

# TAB 2: Ubicación + Condiciones Ambientales
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📍 Ubicación")
        with st.form("form_ubicacion"):
            farm = st.text_input("Nombre de la finca")
            farm_address = st.text_input("Dirección de la finca")
            field_location = st.text_input("Ubicación del lote")
            latitude = st.text_input("Latitud")
            longitude = st.text_input("Longitud")
            soil_type = st.text_input("Tipo de suelo")
            submitted_ubicacion = st.form_submit_button("Guardar Ubicación")
    
    with col2:
        st.header("🌦️ Condiciones Ambientales")
        with st.form("form_ambientales"):
            ambient_temperature = st.number_input("Temperatura ambiente (°C)")
            wind_speed = st.number_input("Velocidad del viento (km/h)")
            relative_humidity = st.number_input("Humedad relativa (%)")
            wind_direction = st.text_input("Dirección del viento")
            ambient_light_intensity = st.number_input("Intensidad de luz")
            submitted_ambientales = st.form_submit_button("Guardar Condiciones")

# TAB 3: Cultivo + Pulverizadora
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🌱 Cultivo")
        with st.form("form_cultivo"):
            crop_specie = st.text_input("Especie del cultivo")
            tillage = st.selectbox("¿Suelo labrado?", ["Sí", "No"])
            row_spacing = st.number_input("Distancia entre hileras")
            crop_population = st.number_input("Población por hectárea")
            crop_stage = st.text_input("Estado fenológico")
            submitted_cultivo = st.form_submit_button("Guardar Cultivo")
    
    with col2:
        st.header("🚜 Pulverizadora")
        with st.form("form_pulverizadora"):
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
            submitted_pulverizadora = st.form_submit_button("Guardar Pulverizadora")

# TAB 4: Colorante + Herbicida + Personal
with tab4:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("💧 Colorante")
        with st.form("form_colorante"):
            dye_used = st.text_input("Tipo de colorante")
            dye_manufacturer = st.text_input("Fabricante")
            dye_concentration = st.number_input("Concentración (%)")
            sensitivity = st.number_input("Sensibilidad")
            tile_size = st.number_input("Tamaño (μm)")
            submitted_colorante = st.form_submit_button("Guardar Colorante")
    
    with col2:
        st.header("🧪 Herbicida")
        with st.form("form_herbicida"):
            herbicide = st.text_input("Nombre del herbicida")
            dose = st.text_input("Dosis aplicada")
            submitted_herbicida = st.form_submit_button("Guardar Herbicida")
    
    with col3:
        st.header("👷 Personal")
        with st.form("form_personal"):
            machine_operator = st.text_input("Operador de la máquina")
            trial_testers = st.text_input("Evaluadores del ensayo")
            submitted_personal = st.form_submit_button("Guardar Personal")

# TAB 5: Modelo de Detección + Resultados Malezas
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🌾 Modelo de Detección")
        with st.form("form_modelo"):
            sens = st.number_input("Sensibilidad")
            tile = st.number_input("Duración del spray abierto")
            submitted_modelo = st.form_submit_button("Guardar Modelo")
    
    with col2:
        st.header("📊 Resultados Malezas")
        with st.form("form_resultados"):
            st.write("Subí un archivo CSV con los datos de malezas")
            csv_file = st.file_uploader("Cargar archivo CSV", type=["csv"])
            uploader = st.text_input("Persona que cargó los datos")
            submitted_resultados = st.form_submit_button("Guardar Resultados")
            
            if submitted_resultados and csv_file:
                df = pd.read_csv(csv_file)
                st.success("Archivo cargado correctamente:")
                st.dataframe(df)