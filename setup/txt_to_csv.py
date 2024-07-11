import pandas as pd

# Define the input and output file paths
input_file_path = 'ocpf/dbo_tPUBLICDOCUMENTS_DOCUMENTS.txt'
output_file_path = 'ocpf/dbo_tPUBLICDOCUMENTS_DOCUMENTS.csv'

# Read the tab-separated text file
data = pd.read_csv(input_file_path, delimiter='\t', encoding="Windows-1252")

# Save the data to a CSV file
data.to_csv(output_file_path, index=False)