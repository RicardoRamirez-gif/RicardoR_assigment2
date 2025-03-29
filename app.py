import streamlit as st
import pandas as pd

# Load the output_list CSV file (it contains the list of editions scraped)
output_list_path = r"C:\Users\Ricardo\Desktop\DOUGLAS COLLEGE COURSES\5_WINTER 2025\CSIS-4260-002--Spl Topics in Data Analytics\RicardoR_assigment2\output_list.csv"
output_list_df = pd.read_csv(output_list_path)

# Strip any leading or trailing spaces from column names
output_list_df.columns = output_list_df.columns.str.strip()

# Load the data from the CSV
output_csv_path = r"C:\Users\Ricardo\Desktop\DOUGLAS COLLEGE COURSES\5_WINTER 2025\CSIS-4260-002--Spl Topics in Data Analytics\RicardoR_assigment2\output_pdf_data.csv"
df = pd.read_csv(output_csv_path)

# Strip any leading or trailing spaces from column names
df.columns = df.columns.str.strip()

# Title of the webpage
st.markdown("<h1 style='text-align: center; color: black;'>Assignment 2 - Scraping Work of Mining Concessions of Chile</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Ricardo Ramirez, Student Id: 300381941</h2>", unsafe_allow_html=True)

# Link to the official Chilean Mining Bulletin webpage
st.markdown("<p style='text-align: center; color: black;'>Official Mining Bulletin of Chile: <a href='https://www.diariooficial.interior.gob.cl/publicaciones/' target='_blank'>www.diariooficial.interior.gob.cl</a></p>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", ["Home", "All Data", "Sentimental Analysis", "Edition Scraption"])

# Main content based on navigation
if selection == "Home":
    st.write(""" 
    ## Home
    This app demonstrates the scraping of mining concession data from the Chilean Official Mining Bulletin (Boletín Oficial de Minería).
    The data includes mining concession names, company names, CVE numbers, regions, provinces, and concession types for mining companies in Chile.
    It also includes sentiment analysis of the available data, allowing us to evaluate the public sentiment related to these concessions.

    ### Project Summary:
    - **PDF Scraping**: Scraped mining concession data (names, companies, CVE numbers, regions, provinces, and concession types) from the Chilean Official Mining Bulletin PDFs.
    - **Sentiment Analysis**: Applied sentiment analysis to evaluate the public sentiment on concession names and regions using Hugging Face's multilingual model.
    - **Web Scraping**: Gathered historical editions of the mining bulletin using **Selenium** and **BeautifulSoup** to track past publications.
    - **Data Visualization**: The extracted data is displayed in an interactive web app using **Streamlit** for users to explore mining concession information.

    **Key Features:**
    - Scraping of detailed data for mining concessions.
    - Sentiment analysis to understand public opinions related to concessions.
    - Historical data on past editions of the Chilean mining bulletin.

    **Libraries Used**:
    - **Requests**, **pdfplumber**, **ftfy**, **BeautifulSoup**, **Selenium**, **transformers**, **Streamlit**, **Pandas**

    The dataset contains detailed information about mining concessions in Chile, and the sentiment analysis evaluates the public sentiment toward these concessions.
    """)

elif selection == "All Data":
    # Modify the title to indicate it's for a specific edition
    st.write("### Sample of Extracted Data - August 1st, 2017 Edition")

    st.write(df)

elif selection == "Sentimental Analysis":
    # Display text explaining sentiment analysis
    st.write(""" 
    ## Sentimental Analysis
    This section would display sentiment analysis results, but the analysis might be limited for mining data due to the nature of the data (i.e., no social media opinions).
    
    ### Part 2: Text Analysis
    In this part, you're required to apply at least two algorithms or APIs to analyze the text data you collected in **Part 1**. Specifically, you're applying **sentiment analysis** to evaluate the public sentiment of mining concessions.

    Here's how you've addressed **Part 2**:
    - **Sentiment Analysis**: You used **Hugging Face's multilingual BERT model** for sentiment analysis on the text data of mining concessions. Sentiment analysis is appropriate for your use case as you're trying to evaluate the public sentiment related to the mining concessions.
    - **Importance Score**: You've assigned an importance score to each mining concession based on sentiment. The scores are mapped to values like -2, -1, 0, 1, and 2, which reflect negative, neutral, and positive sentiments. This gives a clear understanding of how each concession is perceived.
    - **Results in Tabular Form**: The results are displayed in a table, presenting **Concession Name**, **Region Sentiment**, **Concession Sentiment**, and the **Overall Sentiment Score**.

    Additionally, you could apply **keyword extraction**, **topic modeling**, or any other algorithm to analyze the content further. However, sentiment analysis alone is already a solid solution to gauge how concessions are perceived by the public.
    """)

    # Read the sentiment analysis CSV file
    sentiment_data_path = r"C:\Users\Ricardo\Desktop\DOUGLAS COLLEGE COURSES\5_WINTER 2025\CSIS-4260-002--Spl Topics in Data Analytics\RicardoR_assigment2\detailed_analysis_with_concession_sentiment.csv"
    sentiment_df = pd.read_csv(sentiment_data_path)

    # Strip any leading or trailing spaces from column names
    sentiment_df.columns = sentiment_df.columns.str.strip()

    # Display the DataFrame dynamically
    st.write("### Sentiment Analysis Results")
    
    # Show the dataframe as a dynamic table
    st.dataframe(sentiment_df)  # This will display the table and allow sorting/filtering in the UI

elif selection == "Edition Scraption":
    st.write("### Edition Scraption Overview")
    st.write(""" 
    Here we can showcase how the scraping process works for specific editions of the Chilean Official Mining Bulletin (Boletín Oficial de Minería).
    Each edition contains mining concession data, which includes important information such as:
    - Concession Name
    - Company Name
    - CVE Number (Unique ID for each concession)
    - Region
    - Province
    - Concession Type
    
    The editions are scraped from the official website and include concessions for mining companies in Chile.
    """)

    # Display all the editions that were scraped
    st.write("### List of Editions Scraped")
    st.dataframe(output_list_df)

    # Provide a more detailed explanation of the data
    st.write(""" 
    The output list contains all the editions that have been successfully scraped. Each entry represents a particular mining concession record within the given edition of the bulletin. 
    By scraping this data, we have collected a wealth of information on various mining companies, the regions they operate in, and the type of concessions they hold.
    """)

    st.write("### Example of Scraped Data: (Concessions for Each Edition)")
    # Displaying a sample of data for the first edition in the list (if necessary)
    first_edition = output_list_df.iloc[0]
    st.write(f"Edition {first_edition['Edition']} - Date: {first_edition['year']}-{first_edition['month']}-{first_edition['day']}")
    
    # Add a check for 'PDF Link' column and display it only if it exists
    if 'PDF Link' in first_edition:
        st.write("#### PDF Link:", first_edition["PDF Link"])
    else:
        st.write("⚠️ 'PDF Link' column not found. Please check the column name.")

    # Provide an explanation of the scraping process:
    st.write(""" 
    The scraping process involves collecting PDF files from the Chilean Official Mining Bulletin. Each PDF corresponds to a particular edition that includes mining concessions.
    The PDF files are processed to extract mining concession data, including:
    - Company name
    - Concession type (e.g., mining, exploration, etc.)
    - Concession number (CVE Number)
    - Region and province where the concession is located
    
    This data is then stored in a CSV format, allowing us to perform further analysis and present it visually within this app.
    """)

    # Add a section for a downloadable CSV (if needed)
    st.download_button(
        label="Download Scraped Data CSV",
        data=output_list_df.to_csv(index=False),
        file_name='scraped_edition_list.csv',
        mime='text/csv'
    )
