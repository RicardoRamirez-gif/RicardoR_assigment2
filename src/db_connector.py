import os
import streamlit as st
# IMPORTANTE: Se importa 'text' para ejecutar comandos SQL crudos
from sqlalchemy import create_engine, text 
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from dotenv import load_dotenv # Necesario para cargar las variables localmente

# Cargar variables de entorno inmediatamente
load_dotenv()

# --- Database Configuration ---

def get_db_url():
    """Constructs the database connection URL from .env variables."""
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = 'localhost' # Use 'localhost' for local Streamlit run

    if not all([DB_USER, DB_PASSWORD, DB_NAME]):
        return None
        
    # Format: postgresql://user:password@host:port/dbname
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

# --- SQLAlchemy Engine Creation (CORREGIDO CON text()) ---

@st.cache_resource
def get_db_engine():
    """Creates a SQLAlchemy engine for connection pooling."""
    db_url = get_db_url()
    if not db_url:
        st.error("Missing database credentials in .env file. Cannot connect to PostgreSQL.")
        return None
        
    try:
        # Create a connection engine
        engine = create_engine(db_url)
        
        # CORRECCIÓN: Usar text('SELECT 1') para que SQLAlchemy reconozca la consulta
        with engine.connect() as connection:
            connection.execute(text('SELECT 1')) 
        
        return engine
    except SQLAlchemyError as e:
        # Catch specific SQL errors (e.g., incorrect host, bad credentials, Docker not running)
        st.error(f"Database Connection Error: Could not connect to PostGIS container. Ensure Docker is running. Details: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during database connection setup: {e}")
        return None


# --- Data Loading Function (CORREGIDO CON text()) ---

@st.cache_data(ttl=600) 
def load_data_from_db(table_name):
    """
    Loads all data from a specified database table into a Pandas DataFrame.
    """
    engine = get_db_engine()
    if engine is None:
        return pd.DataFrame()

    try:
        query = f"SELECT * FROM {table_name}"
        # CORRECCIÓN: Usar text(query) en pd.read_sql
        df = pd.read_sql(text(query), engine)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        st.success(f"Successfully loaded {len(df)} records from table '{table_name}'.")
        return df
    
    except pd.io.sql.DatabaseError as e:
        st.warning(f"Database Warning: Table '{table_name}' not found. Please run the ETL pipeline first to ingest data. (Details: {e})")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error executing query on table '{table_name}': {e}")
        return pd.DataFrame()