import os
import re
import csv
from bs4 import BeautifulSoup

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# File paths (relative to the script location)
html_file_path = os.path.join(script_dir, "EXTRACT INFO.HTML")
csv_file_path = os.path.join(script_dir, "output_list.csv")

# Read the HTML file
with open(html_file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Find all the links with date and edition information
boletins = []
for div in soup.find_all("div", attrs={"data-date": True}):
    date = div["data-date"]
    link_tag = div.find("a", href=True)
    if link_tag:
        href = link_tag["href"].replace("/?", "")  # Remove leading '/?'
        match = re.search(r"date=(\d{2}-\d{2}-\d{4})&edition=(\d+)", href)
        if match:
            boletins.append([href, match.group(1), match.group(2)])

# Save to CSV
with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Href", "Date", "Edition"])
    writer.writerows(boletins)

print(f"Extracted {len(boletins)} records and saved to {csv_file_path}")
