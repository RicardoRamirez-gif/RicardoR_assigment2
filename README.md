✨ Data Intelligence Pipeline: Chilean Mining Concessions
This repository hosts a scalable Data Engineering pipeline built in Python and containerized with Docker, designed to transform complex, non-structured legal documents into actionable business intelligence.

🎯 Project Goals and Business Value
The primary goal is to automate the full ETL (Extract, Transform, Load) cycle for public mining data, replacing manual parsing and flat-file storage with a robust, scalable data platform.

### Project Goals and Business Value

The primary goal is to **automate the full ETL (Extract, Transform, Load) cycle** for public mining data, replacing manual parsing and flat-file storage with a robust, scalable data platform.

| Value Proposition | Description |
| :--- | :--- |
| **End-to-End ETL** | Automates the complete pipeline from dynamic web navigation and PDF parsing to final database persistence. |
| **Text Analytics** | Integrates advanced Natural Language Processing (NLP) using **Hugging Face** to derive quantitative **Sentiment/Importance Scores** from legal text. |
| **Scalable Data Platform** | Utilizes **Docker** to deploy a Python service integrated with a dedicated **PostgreSQL/PostGIS** database, suitable for advanced geospatial analysis. |

🛠️ Tech Stack & Architecture
Core Technologies
### Core Technologies

| Category | Tools & Libraries |
| :--- | :--- |
| **Data Ingestion** | Python 3.10+, Requests, `pdfplumber`, `ftfy` |
| **Web Automation** | **Playwright** (for dynamic page interaction), Selenium, BeautifulSoup |
| **Data Science** | Pandas, **Hugging Face Transformers** (Multilingual BERT model) |
| **Data Persistence/Infra** | Docker, Docker Compose, PostgreSQL/**PostGIS** |
| **Presentation Layer** | Streamlit (Interactive Web App) |

Code Structure
The project follows the standard modular structure:

/src: Contains all production-ready Python code (extract_pdf_general.py, llm_utils.py, app.py).

/data: Stores local development data/inputs (ignored by .gitignore for data safety and size).

/tests: Contains all unit and functional test scripts.

/docs: Documentation and academic proof (PPTs, video, reports).

🚀 Quick Setup and Execution
The entire platform (Python application and PostGIS database) can be launched using a single Docker Compose command.

Prerequisites: Docker Desktop must be installed and running.

Configure Environment: Create a file named .env in the root directory and define the PostgreSQL and API credentials:

# PostgreSQL Credentials
DB_USER=ricardo_user
DB_PASSWORD=secret_password_123
DB_NAME=mining_data

# API Key for NLP/Summarization
OPENAI_API_KEY=your_key_here
Build and Run the Platform: This command builds the Python service, pulls the PostGIS image, and starts both containers.

Bash

docker-compose up -d --build
The ETL application will execute automatically upon container startup, scrape the index data, and ingest the results directly into the PostGIS database service.

Verify Data Persistence: Access the PostgreSQL container to run SQL queries or connect a geospatial tool to port 5432 using the credentials from .env.

Run the Dashboard (Optional): Once the ETL has run, you can launch the Streamlit dashboard locally to view the results:

Bash

streamlit run src/app.py
📸 Visual Demonstration
To illustrate the pipeline's capabilities, consider adding these visual assets to your repository's root (e.g., in an /assets folder).