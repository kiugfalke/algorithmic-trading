import requests
import pandas as pd

# URL API IMF
BASE_URL = "https://dataservices.imf.org/REST/SDMX_JSON.svc/"
DATASET_CODE = "CompactData/IFS"

# Indicadores clave para EUR/USD
INDICATORS = ["NGDP_R", "PCPI_IX", "EREER_IX", "IR_SR_IX"]  # PIB, Inflación, Tipo de Cambio, Tasa de interés

def fetch_imf_data(country_code="US", start_year="2000", end_year="2025"):
    """ Obtiene datos macroeconómicos clave para señal en Forex """
    url = f"{BASE_URL}{DATASET_CODE}/{country_code}/{','.join(INDICATORS)}/{start_year}/{end_year}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Error al conectar con la API: {response.status_code}")
        return pd.DataFrame()

    try:
        data = response.json()["CompactData"]["DataSet"]["Series"]
        df = pd.DataFrame()

        for series in data:
            indicator = series["@VAR"]
            values = series["Obs"]
            temp_df = pd.DataFrame(values)
            temp_df["Indicator"] = indicator
            df = pd.concat([df, temp_df], ignore_index=True)

        df.rename(columns={"@TIME_PERIOD": "Year", "@OBS_VALUE": "Value"}, inplace=True)
        df["Year"] = pd.to_datetime(df["Year"], format="%Y")
        df.sort_values(by="Year", inplace=True)
        return df

    except KeyError:
        print("❌ Error procesando los datos obtenidos.")
        return pd.DataFrame()

if __name__ == "__main__":
    imf_data = fetch_imf_data("US")  # Datos de EE.UU. para EUR/USD
    print("🔍 Análisis Fundamental para EUR/USD:")
    print(imf_data.head())