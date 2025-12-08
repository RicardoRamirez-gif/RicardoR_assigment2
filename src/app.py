import streamlit as st
import pandas as pd
import os
import io

# --- NUEVO: Carga Forzada de .env ---
from dotenv import load_dotenv

# Cargar variables de entorno inmediatamente al inicio de la app
load_dotenv()
# ------------------------------------

# Import the database connector...
from db_connector import load_data_from_db

# --- FIX: Direct Import to resolve 'ImportError' ---
# Change: from .db_connector import load_data_from_db 
# To: (Assumes db_connector.py is in the same folder, src/)
from db_connector import load_data_from_db

# --- DATA LOADING FROM POSTGRESQL ---
# The names of the tables assumed to be populated by the Dockerized ETL runner:
TABLE_EDITIONS = 'editions_list'
TABLE_CONCESSIONS = 'mining_concessions' 
TABLE_SENTIMENT = 'sentiment_metrics' 

# Load dataframes from the database connection
# This replaces the entire old CSV loading logic
output_list_df = load_data_from_db(TABLE_EDITIONS)
df = load_data_from_db(TABLE_CONCESSIONS)
sentiment_df = load_data_from_db(TABLE_SENTIMENT)

# --- WEB APP STRUCTURE ---

# Title of the webpage (Professional Focus)
st.markdown("<h1 style='text-align: center;'>Chilean Mining Concession Data Intelligence ⛏️</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Automated ETL and Text Analytics Platform</h4>", unsafe_allow_html=True)

# Link to the official Chilean Mining Bulletin webpage (FIXED URL)
st.markdown("<p style='text-align: center;'>Data Source: <a href='https://www.diariooficial.interior.gob.cl/' target='_blank'>Official Mining Bulletin of Chile</a></p>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title('Pipeline Navigation')
selection = st.sidebar.radio("Go to", ["Home", "Extracted Data", "Text Analysis Metrics", "Edition Tracking"])

# --- FUTURE STATE MESSAGE (Now dynamic and accurate) ---
st.sidebar.markdown(
    """
    ***
    **Data Persistence:** Data persistence is handled by a **PostgreSQL/PostGIS** database, accessible via port 5432.
    """
)

# Main content based on navigation
if selection == "Home":
    st.write(""" 
    ## Data Pipeline Overview
    This application demonstrates a **full-cycle Data Engineering and NLP pipeline** designed to convert complex, non-structured legal documents into actionable business intelligence.

    ### Project Summary:
    - **PDF Scraping & Parsing**: Automated extraction of critical data (names, regions, CVE numbers) from dynamic Chilean Official Mining Bulletin PDFs.
    - **Web Scraping**: Uses **Selenium** and **BeautifulSoup** to gather and track historical editions of the bulletin, ensuring data integrity.
    - **Text Analysis & Metrics**: Applied **Hugging Face's multilingual model** to derive **Sentiment Scores** and evaluate public perception on concession names and regions.
    - **Data Visualization**: Interactive data display using **Streamlit**, proving the end-to-end functionality of the platform.

    **Libraries Used**:
    - **Selenium**, **BeautifulSoup**, **Pandas**, **pdfplumber**, **requests**, **Streamlit**, **transformers** (for NLP)
    """)

elif selection == "Extracted Data":
    st.write("### Extracted Concession Data Sample")
    st.write("A sample of the structured data ingested directly from the PostgreSQL database.")

    if not df.empty:
        st.dataframe(df)
    else:
        st.warning(f"Data not available. Please ensure the ETL pipeline has successfully loaded data into the '{TABLE_CONCESSIONS}' table.")

elif selection == "Text Analysis Metrics":
    st.write(""" 
    ## Text Analysis & Sentiment Metrics
    This section showcases the **transformation layer (T)** of the ETL, where unstructured text is converted into quantifiable metrics.

    ### Metric Generation:
    - **Sentiment Analysis**: Applied **Hugging Face's multilingual BERT model** to assign sentiment (positive, neutral, negative) to concession names and regions.
    - **Importance Scoring**: A structured score is mapped (-2 to +2), providing a clear, quantitative gauge of public perception for each mining asset.
    - **Output**: The results are presented in a clean, query-ready format for further spatial or economic analysis.
    """)

    if not sentiment_df.empty:
        st.write("### Sentiment Analysis Results (From PostGIS)")
        st.dataframe(sentiment_df)
    else:
        st.warning(f"Sentiment data not available. Please check the data loading from the '{TABLE_SENTIMENT}' table.")

elif selection == "Edition Tracking":
    st.write("### Bulletin Edition Tracking")
    st.write("Overview of the historical editions successfully scraped, demonstrating the stability of the Web Scraping process.")

    if not output_list_df.empty:
        st.dataframe(output_list_df)

        st.write("#### Download Data Snapshot")
        # NOTE: Keeping CSV Download as a feature, even if data comes from DB
        @st.cache_data
        def convert_df_to_csv(df_to_convert):
            return df_to_convert.to_csv(index=False).encode('utf-8')

        csv_data = convert_df_to_csv(output_list_df)

        st.download_button(
            label="Download Editions CSV",
            data=csv_data,
            file_name='edition_tracking_snapshot.csv',
            mime='text/csv'
        )
    else:
        st.warning(f"Edition tracking data not available. Please check the '{TABLE_EDITIONS}' table.")