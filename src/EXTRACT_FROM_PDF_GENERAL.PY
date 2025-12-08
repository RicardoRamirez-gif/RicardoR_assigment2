import re
import csv
import requests
import pdfplumber
import ftfy
import os
from io import BytesIO

# Import the LLM utility module
# from .llm_utils import summarize_text 

# --- PORTABLE PATHS (Assumes data is in ../data/) ---
# Note: Input path (output_list.csv) and Output path (output_pdf_data_total.csv)
# We use os.path.join and relative paths for robustness.
INPUT_CSV_PATH = os.path.join("..", "data", "output_list.csv")
OUTPUT_CSV_PATH = os.path.join("..", "data", "output_pdf_data_total.csv")
# ----------------------------------------------------

# Keywords to identify sections
concession_types = [
    "PEDIMENTOS MINEROS", "MANIFESTACIONES", "SOLICITUDES DE MENSURA",
    "EXTRACTOS DE SENTENCIA DE EXPLORACIÓN", "EXTRACTOS DE SENTENCIA DE EXPLOTACIÓN"
]

# Regular expressions
region_pattern = r"([IVXLCDM]+)\s+REGIÓN\s+DE\s+([A-ZÁÉÍÓÚÑ\s]+)"
province_pattern = r"Provincia de ([A-Za-zÁÉÍÓÚÑ\s]+)"
mining_pattern = r"(.+?)\s*/\s*(.+?)\s*\(CVE:\s*(\d+)\)"

# --- PDF DOWNLOAD AND EXTRACTION LOGIC ---

def download_pdf(url: str) -> BytesIO | None:
    """Downloads PDF content from a URL and returns a BytesIO object."""
    try:
        # Use a more reasonable timeout for production scenarios
        response = requests.get(url, timeout=30) 
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading PDF: {e}")
        return None

def extract_text_from_pdf(pdf_file: BytesIO) -> str:
    """Extracts text from a BytesIO PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text(x_tolerance=3, y_tolerance=3)
                if extracted_text:
                    fixed_text = ftfy.fix_encoding(extracted_text.strip())
                    text += fixed_text + "\n"
        return text.encode("utf-8", errors="replace").decode("utf-8")
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return ""

# --- PARSING LOGIC (Remains the same, but cleaner syntax) ---

def parse_pdf_text(text: str, source_url: str) -> list[list[str]]:
    """Parses raw PDF text to extract structured mining concession data."""
    data = []
    current_region, current_province, current_type = "", "", ""
    
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        
        region_match = re.search(region_pattern, line, re.IGNORECASE)
        if region_match:
            current_region = region_match.group(2).strip()
        
        province_match = re.search(province_pattern, line)
        if province_match:
            current_province = province_match.group(1).strip()
        
        for concession in concession_types:
            if concession in line:
                current_type = concession
                break
        
        mining_match = re.search(mining_pattern, line)
        if mining_match:
            concession_name = mining_match.group(1).strip()
            company_name = mining_match.group(2).strip()
            cve_number = mining_match.group(3).strip()
            
            # TODO: Integrate LLM summarization here if needed: summary = summarize_text(concession_name)
            
            data.append([concession_name, company_name, cve_number,
                         current_region, current_province, current_type, source_url])
    
    return data

# --- DATA READING AND WRITING (TO BE REPLACED BY DB INGEST) ---

def read_pdf_list(csv_path: str) -> list[str]:
    """Reads the CSV index file containing PDF URLs to process."""
    pdf_list = []
    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Reconstruct the PDF URL from structured components
                year, month, day, edition = row["year"], row["month"], row["day"], row["Edition"]
                # URL is hardcoded as it is a fixed domain/structure of the official bulletin
                pdf_url = f"https://www.diariooficial.interior.gob.cl/publicaciones/{year}/{month}/{day}/sumarios/{edition}.pdf"
                pdf_list.append(pdf_url)
    except Exception as e:
        print(f"❌ Error reading input CSV: {e}")
    return pdf_list

def write_to_csv(data: list[list[str]], output_path: str, append: bool = False):
    """Writes extracted data to CSV (THIS FUNCTION WILL BE REPLACED BY DB INGEST)."""
    headers = ["Nombre de la Concesión", "Nombre de la Empresa", "Número CVE", "Región", "Provincia", "Tipo de Concesión", "Fuente"]
    try:
        mode = 'a' if append else 'w'
        with open(output_path, mode, newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not append:
                writer.writerow(headers) 
            writer.writerows(data)
        print(f"✅ Data saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

# --- MAIN RUNNER ---

def process_pdfs_pipeline(pdf_urls: list[str], output_csv_path: str):
    """Runs the main PDF processing pipeline (Extraction -> Parsing -> Load)."""
    write_to_csv([], output_csv_path, append=False) # Clear file with headers
    
    for pdf_url in pdf_urls:
        print(f"📥 Processing: {pdf_url}")
        pdf_file = download_pdf(pdf_url)
        if pdf_file:
            pdf_text = extract_text_from_pdf(pdf_file)
            if pdf_text:
                extracted_data = parse_pdf_text(pdf_text, pdf_url)
                if extracted_data:
                    # NOTE: Here is where the LLM/Sentiment logic (if enabled) would run
                    write_to_csv(extracted_data, output_csv_path, append=True) 
                else:
                    print("⚠ No relevant data found in this PDF.")
            else:
                print("⚠ Could not extract text.")
        else:
            print("⚠ Could not download the PDF.")

if __name__ == "__main__":
    pdf_urls = read_pdf_list(INPUT_CSV_PATH)
    process_pdfs_pipeline(pdf_urls, OUTPUT_CSV_PATH)