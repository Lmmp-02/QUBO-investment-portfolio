import pandas as pd
import os
from datetime import timedelta

# Directorio donde se encuentran los archivos .txt
directory = 'Dataset_Grande/Stocks'

# Obtener la lista de archivos .txt en el directorio
all_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

# Lista para almacenar los dataframes
dataframes = []

# Leer cada archivo y extraer las columnas necesarias
for file in all_files[:100]:  # Limit to first 200 files
    file_path = os.path.join(directory, file)
    try:
        df = pd.read_csv(file_path, usecols=['Date', 'Open', 'Close'])
        # Convert 'Date' column to datetime format, specify format if necessary
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')

        if df.empty:
            continue

        # Find the most recent date in the dataset
        max_date = df['Date'].max()
        # Calculate the date two years before the most recent date
        two_years_before_max = max_date - timedelta(days=2*365)

        # Filter data from two years before the most recent date to the most recent date
        df_filtered = df[(df['Date'] >= two_years_before_max) & (df['Date'] <= max_date)]

        if not df_filtered.empty:
            # Sort data by date in descending order
            df_filtered.sort_values(by='Date', ascending=False, inplace=True)
            # Add a column with the company name
            df_filtered['Company'] = os.path.splitext(file)[0]
            # Reorder columns so 'Company' is first
            df_filtered = df_filtered[['Company', 'Date', 'Open', 'Close']]
            dataframes.append(df_filtered)
    except (pd.errors.EmptyDataError, KeyError) as e:
        print(f"Error processing file {file}: {e}")

# Concatenate all dataframes
if dataframes:
    result_df = pd.concat(dataframes, ignore_index=True)
    # Display the first rows of the resulting DataFrame
    print(result_df.head())
    # Save the resulting DataFrame to a CSV file if needed
    result_df.to_csv('Dataset_Grande_Procesado.csv', index=False)
else:
    print("No se encontraron archivos con datos válidos.")
