import requests
import pandas as pd

# URL de la API del IMF
base_url = "https://dataservices.imf.org/REST/SDMX_JSON.svc/"

# Código de dataset para International Financial Statistics (IFS)
dataset_code = "IFS"

# Definir consulta con indicadores específicos
params = {
    "startPeriod": "2000",
    "endPeriod": "2025",
    "dimensionAtObservation": "TIME",
}

# Realizar solicitud a la API
response = requests.get(f"{base_url}{dataset_code}", params=params)

# Verificar si la conexión fue exitosa
if response.status_code == 200:
    data = response.json()
    print("✅ Datos recibidos correctamente!")
else:
    print("❌ Error al conectar con la API:", response.status_code)