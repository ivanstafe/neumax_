import firebase_admin
from firebase_admin import credentials, firestore, auth
import os


# Ruta al archivo JSON con las credenciales
cred_path = os.path.join(os.path.dirname(__file__), 'registro-gomeria-firebase-adminsdk-hwrjn-ee569a0bcb.json')

# Verifica si el archivo realmente existe en la ruta especificada
if not os.path.exists(cred_path):
    raise FileNotFoundError(f"El archivo de credenciales no se encuentra en la ruta: {cred_path}")

# Inicializa la aplicación Firebase
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Conectar a la base de datos Firestore
db = firestore.client()
auth_client = auth
