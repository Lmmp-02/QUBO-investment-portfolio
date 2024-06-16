import pandas as pd
import os

# Directorio donde se encuentran los archivos .txt
directory = 'Dataset_Grande/Stocks'  # Ruta actualizada para apuntar a la carpeta correcta

# Obtener la lista de archivos .txt en el directorio
all_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

# Tomar solo los primeros 1000 archivos
files_to_read = all_files[:1000]

# Lista para almacenar los dataframes
dataframes = []

# Leer cada archivo y extraer las columnas necesarias
for file in files_to_read:
    file_path = os.path.join(directory, file)
    try:
        # Verificar que el archivo no esté vacío y contenga las columnas necesarias
        df = pd.read_csv(file_path, nrows=1)  # Leer solo la primera fila para verificar
        if set(['Date', 'Open', 'Close']).issubset(df.columns):
            # Leer el archivo completo si tiene las columnas necesarias
            df = pd.read_csv(file_path, usecols=['Date', 'Open', 'Close'])
            # Agregar una columna con el nombre de la empresa
            df['Company'] = os.path.splitext(file)[0]
            # Reorganizar las columnas para que 'Company' esté al principio
            df = df[['Company', 'Date', 'Open', 'Close']]
            dataframes.append(df)
        else:
            print(f"Archivo {file} no contiene las columnas necesarias.")
    except pd.errors.EmptyDataError:
        print(f"Archivo {file} está vacío y ha sido omitido.")

# Concatenar todos los dataframes
if dataframes:
    result_df = pd.concat(dataframes, ignore_index=True)
    # Mostrar las primeras filas del DataFrame resultante
    print(result_df.head())
    # Guardar el DataFrame resultante en un archivo CSV si es necesario
    result_df.to_csv('Dataset_Grande_Procesado.csv', index=False)
else:
    print("No se encontraron archivos con datos válidos.")
