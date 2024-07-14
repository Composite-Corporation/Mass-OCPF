import sqlite3
import pandas as pd

# Load the CSV files
print("Loading CSV files...")
keywords_df = pd.read_csv('data/dbo_tPUBLICDOCUMENTS_DOCUMENT_KEYWORDS.csv')
documents_df = pd.read_csv('data/dbo_tPUBLICDOCUMENTS_DOCUMENTS.csv')
document_keywords_df = pd.read_csv('data/dbo_tPUBLICDOCUMENTS_KEYWORDS.csv')

# Create an SQLite database connection
conn = sqlite3.connect('public_documents.db')
cursor = conn.cursor()

# Create tables
print("Creating SQL tables...")
cursor.execute('''
    CREATE TABLE dbo_tPUBLICDOCUMENTS_DOCUMENTS (
        Public_Document_ID INTEGER PRIMARY KEY,
        Public_Document_Type_ID INTEGER,
        Public_Document_Code TEXT,
        Title TEXT,
        Description TEXT,
        Body TEXT,
        URL TEXT,
        Is_Public INTEGER,
        Date TEXT,
        Document_Status_Type_ID INTEGER,
        Subject_Name TEXT,
        Legal_Genesis TEXT,
        Guidance_Issues TEXT,
        Update_Information TEXT,
        Date_Revised TEXT,
        Guidance_Comments TEXT,
        Ordinal INTEGER,
        Doc_Suffix TEXT,
        Year_Section INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE dbo_tPUBLICDOCUMENTS_DOCUMENT_KEYWORDS (
        Public_Document_Keyword_ID INTEGER PRIMARY KEY,
        Public_Document_ID INTEGER,
        Keyword_ID INTEGER,
        Keyword_Weight INTEGER,
        Keyword_Category_ID INTEGER,
        FOREIGN KEY (Public_Document_ID) REFERENCES dbo_tPUBLICDOCUMENTS_DOCUMENTS(Public_Document_ID),
        FOREIGN KEY (Keyword_ID) REFERENCES dbo_tPUBLICDOCUMENTS_KEYWORDS(Keyword_ID)
    )
''')

cursor.execute('''
    CREATE TABLE dbo_tPUBLICDOCUMENTS_KEYWORDS (
        Keyword_ID INTEGER PRIMARY KEY,
        Keyword_Description TEXT,
        Keyword_Category_ID INTEGER
    )
''')

# Load data into tables
print("Inserting rows to SQL database...")
keywords_df.to_sql('dbo_tPUBLICDOCUMENTS_DOCUMENT_KEYWORDS', conn, if_exists='append', index=False)
documents_df.to_sql('dbo_tPUBLICDOCUMENTS_DOCUMENTS', conn, if_exists='append', index=False)
document_keywords_df.to_sql('dbo_tPUBLICDOCUMENTS_KEYWORDS', conn, if_exists='append', index=False)

# Commit the transaction
conn.commit()

# Verify by querying the database
print("Executing sample queries...")
cursor.execute('SELECT * FROM dbo_tPUBLICDOCUMENTS_DOCUMENTS LIMIT 5')
documents_sample = cursor.fetchall()

cursor.execute('SELECT * FROM dbo_tPUBLICDOCUMENTS_DOCUMENT_KEYWORDS LIMIT 5')
document_keywords_sample = cursor.fetchall()

cursor.execute('SELECT * FROM dbo_tPUBLICDOCUMENTS_KEYWORDS LIMIT 5')
keywords_sample = cursor.fetchall()

# Close the connection
conn.close()

print("Sample data from dbo_tPUBLICDOCUMENTS_DOCUMENTS:", documents_sample)
print("Sample data from dbo_tPUBLICDOCUMENTS_DOCUMENT_KEYWORDS:", document_keywords_sample)
print("Sample data from dbo_tPUBLICDOCUMENTS_KEYWORDS:", keywords_sample)
