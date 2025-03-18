import requests

pdf_url = "https://www.diariooficial.interior.gob.cl/publicaciones/2017/08/01/sumarios/41823.pdf"

try:
    response = requests.get(pdf_url)
    response.raise_for_status()
    with open("test.pdf", "wb") as f:
        f.write(response.content)
    print("✅ PDF downloaded successfully!")
except requests.exceptions.RequestException as e:
    print(f"❌ Error: {e}")
