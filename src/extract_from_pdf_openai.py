import openai
import re
import csv
import requests
import pdfplumber
import ftfy
from io import BytesIO

# Set OpenAI API Key
openai.api_key = 'your_openai_api_key'

# PDF URL
pdf_url = "https://www.diariooficial.interior.gob.cl/publicaciones/2017/08/01/sumarios/41823.pdf"

# Output CSV file
output_csv_path = r"C:\Users\Ricardo\Desktop\DOUGLAS COLLEGE COURSES\5_WINTER 2025\CSIS-4260-002--Spl Topics in Data Analytics\RicardoR_assigment2\output_pdf_data.csv"

# Keywords to identify sections
concession_types = [
    "PEDIMENTOS MINEROS", "MANIFESTACIONES", "SOLICITUDES DE MENSURA",
    "EXTRACTOS DE SENTENCIA DE EXPLORACIÓN", "EXTRACTOS DE SENTENCIA DE EXPLOTACIÓN"
]

# Regular expressions
region_pattern = r"([IVXLCDM]+)\s+REGIÓN\s+DE\s+([A-ZÁÉÍÓÚÑ\s]+)"
province_pattern = r"Provincia de ([A-Za-zÁÉÍÓÚÑ\s]+)"
mining_pattern = r"(.+?)\s*/\s*(.+?)\s*\(CVE:\s*(\d+)\)"

# Function to download PDF
def download_pdf(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading PDF: {e}")
        return None

# Function to extract text using pdfplumber
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text(x_tolerance=3, y_tolerance=3)
                if extracted_text:
                    # Fix encoding issues
                    fixed_text = ftfy.fix_encoding(extracted_text.strip())
                    text += fixed_text + "\n"
        return text.encode("utf-8", errors="replace").decode("utf-8")  # Convert safely
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return ""

# Function to summarize text using OpenAI API
def summarize_text(text):
    try:
        # Send the extracted text to OpenAI's GPT model for summarization
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following text:\n\n{text}",
            max_tokens=150,  # Limit the length of the summary
            n=1,
            stop=None,
            temperature=0.7
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print(f"❌ Error summarizing text: {e}")
        return ""

# Function to parse text
def parse_pdf_text(text):
    data = []
    current_region, current_province, current_type = "", "", ""

    lines = text.split("\n")
    for line in lines:
        line = line.strip()

        # Detect region
        region_match = re.search(region_pattern, line, re.IGNORECASE)
        if region_match:
            current_region = region_match.group(2).strip()

        # Detect province
        province_match = re.search(province_pattern, line)
        if province_match:
            current_province = province_match.group(1).strip()

        # Detect concession type
        for concession in concession_types:
            if concession in line:
                current_type = concession
                break

        # Detect mining entries
        mining_match = re.search(mining_pattern, line)
        if mining_match:
            concession_name = mining_match.group(1).strip()
            company_name = mining_match.group(2).strip()
            cve_number = mining_match.group(3).strip()

            # Create a list of relevant data to be summarized later
            data.append([concession_name, company_name, cve_number, current_region, current_province, current_type])

    return data

# Function to write CSV
def write_to_csv(data, output_path):
    headers = ["Nombre de la Concesión", "Nombre de la Empresa", "Número CVE", "Región", "Provincia", "Tipo de Concesión", "Summary"]
    try:
        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"✅ Data saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

# Run script
if __name__ == "__main__":
    pdf_file = download_pdf(pdf_url)
    if pdf_file:
        pdf_text = extract_text_from_pdf(pdf_file)
        if pdf_text:
            extracted_data = parse_pdf_text(pdf_text)
            if extracted_data:
                # Summarize the content using OpenAI API
                summarized_data = []
                for row in extracted_data:
                    summary = summarize_text(row[0])  # Using the 'concession_name' as the text to summarize
                    row.append(summary)  # Add the summary to the row
                    summarized_data.append(row)
                
                write_to_csv(summarized_data, output_csv_path)
            else:
                print("⚠ No relevant data found.")
        else:
            print("⚠ Could not extract text.")
    else:
        print("⚠ Could not download the PDF.")
