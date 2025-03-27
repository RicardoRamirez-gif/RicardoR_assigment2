import re
import csv
import requests
import pdfplumber
import ftfy
from io import BytesIO

# Input CSV containing the list of PDFs to process
input_csv_path = r"C:\Users\Ricardo\Desktop\DOUGLAS COLLEGE COURSES\5_WINTER 2025\CSIS-4260-002--Spl Topics in Data Analytics\RicardoR_assigment2\output_list.csv"

# Output CSV for extracted data
output_csv_path = r"C:\Users\Ricardo\Desktop\DOUGLAS COLLEGE COURSES\5_WINTER 2025\CSIS-4260-002--Spl Topics in Data Analytics\RicardoR_assigment2\output_pdf_data_total.csv"

# Keywords to identify sections
concession_types = [
    "PEDIMENTOS MINEROS", "MANIFESTACIONES", "SOLICITUDES DE MENSURA",
    "EXTRACTOS DE SENTENCIA DE EXPLORACIÓN", "EXTRACTOS DE SENTENCIA DE EXPLOTACIÓN"
]

# Regular expressions
region_pattern = r"([IVXLCDM]+)\s+REGIÓN\s+DE\s+([A-ZÁÉÍÓÚÑ\s]+)"
province_pattern = r"Provincia de ([A-Za-zÁÉÍÓÚÑ\s]+)"
mining_pattern = r"(.+?)\s*/\s*(.+?)\s*\(CVE:\s*(\d+)\)"

def download_pdf(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading PDF: {e}")
        return None

def extract_text_from_pdf(pdf_file):
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

def parse_pdf_text(text, source_url):
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
            
            data.append([concession_name, company_name, cve_number,
                         current_region, current_province, current_type, source_url])
    
    return data

def read_pdf_list(csv_path):
    pdf_list = []
    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                year, month, day, edition = row["year"], row["month"], row["day"], row["Edition"]
                pdf_url = f"https://www.diariooficial.interior.gob.cl/publicaciones/{year}/{month}/{day}/sumarios/{edition}.pdf"
                pdf_list.append(pdf_url)
    except Exception as e:
        print(f"❌ Error reading input CSV: {e}")
    return pdf_list

def write_to_csv(data, output_path, append=False):
    headers = ["Nombre de la Concesión", "Nombre de la Empresa", "Número CVE", "Región", "Provincia", "Tipo de Concesión", "Fuente"]
    try:
        # Open the file in append mode if `append` is True
        mode = 'a' if append else 'w'
        with open(output_path, mode, newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not append:
                writer.writerow(headers)  # Write headers only once when appending
            writer.writerows(data)
        print(f"✅ Data saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

# Main processing loop: Write data after each PDF
def process_pdfs(pdf_urls, output_csv_path):
    for pdf_url in pdf_urls:
        print(f"📥 Processing: {pdf_url}")
        pdf_file = download_pdf(pdf_url)
        if pdf_file:
            pdf_text = extract_text_from_pdf(pdf_file)
            if pdf_text:
                extracted_data = parse_pdf_text(pdf_text, pdf_url)
                if extracted_data:
                    write_to_csv(extracted_data, output_csv_path, append=True)  # Append data after processing each PDF
                else:
                    print("⚠ No relevant data found in this PDF.")
            else:
                print("⚠ Could not extract text.")
        else:
            print("⚠ Could not download the PDF.")

# Run the processing function
if __name__ == "__main__":
    pdf_urls = read_pdf_list(input_csv_path)
    process_pdfs(pdf_urls, output_csv_path)
