# src/boletin_records.py (Líneas iniciales)
import os
import pandas as pd
from sqlalchemy import create_engine
from playwright.sync_api import sync_playwright

# --- FIX: CARGA DE VARIABLES DE ENTORNO EN EL ETL ---
from dotenv import load_dotenv

# Cargar variables de entorno inmediatamente
load_dotenv()
# ----------------------------------------------------

# --- CONFIGURACIÓN DE HOST DE DB PARA DOCKER ---
DB_HOST = 'db' # Nombre del servicio DB en docker-compose.yml
DB_TABLE = 'editions_list' # Nombre de la tabla para el índice de ediciones
# Importamos la librería 'text' aunque no la usemos aquí, es buena práctica si usamos SQL crudo
# from sqlalchemy.sql import text 

# --- CONFIGURACIÓN DE HOST DE DB PARA DOCKER ---
DB_HOST = 'db' # Nombre del servicio DB en docker-compose.yml
DB_TABLE = 'editions_list' 

def get_etl_engine():
    """Engine for the ETL app (running inside Docker, connecting to 'db' service)."""
    # Las variables de entorno son leídas automáticamente por el contenedor de Docker
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    
    # URL apuntando al servicio 'db'
    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    return create_engine(db_url)


def load_data_to_postgres(df: pd.DataFrame, table_name: str):
    """Saves DataFrame to the PostGIS container."""
    engine = get_etl_engine()
    
    try:
        print(f"INFO: Attempting to create/replace table: {table_name}")
        
        # Uso de pd.to_sql: crea la tabla y la carga.
        df.to_sql(
            table_name, 
            con=engine, 
            if_exists='replace', # Crea la tabla si no existe, o la reemplaza
            index=False,
            chunksize=1000
        )
        print(f"SUCCESS: Table {table_name} created and loaded successfully.")

    except Exception as e:
        # Esto atrapará errores de conexión, credenciales o tablas
        print(f"FATAL DB ERROR: Could not load table {table_name}. Details: {e}")
        raise # Re-lanza el error para que Docker sepa que el ETL falló

# --- FUNCIÓN PRINCIPAL DE SCRAPING ---

def extract_boletin_info(target_url: str):
    """Core function to scrape index data from the Boletín Oficial."""
    # ... (omito el código Playwright, asumiendo que ya funciona)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(target_url, timeout=120000)
            page.wait_for_load_state("networkidle") 

            boletin_number_full = page.locator('.containerdate .alignleft').inner_text().strip()
            date = page.locator('.containerdate .date strong').inner_text().strip()
            pdf_link = page.locator('.containerdate .alignright a.summary').get_attribute('href')
            
            boletin_number = boletin_number_full.replace("Edición Núm.", "").strip()

            # 3. Preparación y Carga a la DB (ETL Flow)
            # Creamos un DataFrame con la lista de ediciones (Tabla 1)
            editions_data = {
                "boletin_number": [boletin_number],
                "date": [date],
                "pdf_link": [pdf_link],
                # Agrega columnas necesarias para uniones o filtros (Ejemplo)
                "year": [date.split()[2]], 
                "edition_id": [boletin_number]
            }
            df_editions = pd.DataFrame(editions_data)

            # CARGA DE LA TABLA 1 (editions_list)
            load_data_to_postgres(df_editions, 'editions_list')

            # --- Placeholder para las otras tablas ---
            # Para que la Streamlit App funcione, necesitamos las otras tablas, aunque estén vacías
            
            # Tabla 2: Concesiones
            df_concessions = pd.DataFrame(columns=['id', 'concession_name', 'company', 'region'])
            load_data_to_postgres(df_concessions, 'mining_concessions')

            # Tabla 3: Sentimientos
            df_sentiment = pd.DataFrame(columns=['id', 'concession_name', 'sentiment_score'])
            load_data_to_postgres(df_sentiment, 'sentiment_metrics')
            
        except Exception as e:
            print(f"CRITICAL ERROR during scraping {target_url}: {e}")
            raise # Re-lanza el error para que el contenedor falle si hay problemas
        finally:
            browser.close()

if __name__ == "__main__":
    # La URL de prueba está aquí, pero en un entorno real debe ser dinámica.
    TEST_URL = "https://www.boletinoficialdemineria.cl/?date=11-03-2025&edition=44096"
    extract_boletin_info(TEST_URL)