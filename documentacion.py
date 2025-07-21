'''
# 📦 Utilizar MongoDB en Python con PyMongo

# 1. Importar la librería
from pymongo import MongoClient

# 2. Conexión a MongoDB local (puerto por defecto: 27017)
client = MongoClient("mongodb://localhost:27017")

# 3. Seleccionar base de datos y colección
db = client["ensayos_db"]           # Base de datos
coleccion = db["formularios"]       # Colección (equivalente a una tabla)

# 4. Guardar datos en la colección
if submitted_cliente:
    coleccion.insert_one({
        "seccion": "cliente",
        "nombre": name,
        "sprai_id": sprai_id,
        "modules_id": modules_id
    })
    st.success("✅ Cliente guardado correctamente")

# 🛠 Instalación y configuración de MongoDB en Linux

# 1. Instalar MongoDB (repositorio oficial recomendado en producción)
sudo apt install -y mongodb-org

# 2. Iniciar y habilitar el servicio
sudo systemctl start mongod          # Inicia el servicio
sudo systemctl enable mongod         # Lo activa al iniciar el sistema
sudo systemctl status mongod         # Verifica que está corriendo

# 🧪 Probar que MongoDB funciona correctamente

mongosh                             # Entra a la consola de MongoDB

use test                            # Cambia o crea base de datos "test"
db.prueba.insertOne({ saludo: "Hola MongoDB desde Linux" })  # Inserta
db.prueba.find()                   # Muestra los datos
'''

