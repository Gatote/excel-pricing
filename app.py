import streamlit as st
import pandas as pd

# Configuración de layout en Streamlit
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Visor de Excel")

# Subir archivo Excel
uploaded_file = st.file_uploader("Sube tu archivo de Excel", type=["xlsx"])

# Lista de SKUs predeterminados (asegurarse de que todos sean cadenas)
default_skus = [
    '409', 'Z43', 'Z45', '206', '207',
    'L58', '179', '264', 'Z89', 'F19', 'Q92',
    '410', '193', '131', 'L32', 'F46',
    '403', 'E82', '25', '356', '357', '405',
    '146', 'U26', 'U25', '108', 'G22', '371', 'T63',
    '318', 'Z52', '21', '978', 'E05',
    '791'
]

# Verificar si se ha subido un archivo
if uploaded_file is not None:
    # Cargar el archivo Excel
    excel_data = pd.ExcelFile(uploaded_file)
    
    # Seleccionar la hoja del archivo
    sheet_name = st.selectbox("Selecciona una hoja", excel_data.sheet_names)

    # Leer la hoja seleccionada
    df = excel_data.parse(sheet_name)
    
    # Eliminar filas vacías al principio y al final (si las hay)
    df = df.dropna(how='all')  # Eliminar filas vacías completamente
    
    # Seleccionar solo las primeras 9 columnas, ya que no necesitas más
    df = df.iloc[:, :9]  # Seleccionar solo las primeras 9 columnas
    
    # Definir los nombres de las columnas manualmente
    manual_headers = [
        'Primal', 'SKU', 'SQL', 'NAM', 'Description', 
        'box / pallet', '1 - 9 pallets (DL/LB)', '10 - 19 pallets (DL/LB)', '+ 20 pallets (DL/LB)'
    ]
    
    # Asignar los encabezados manuales al DataFrame
    df.columns = manual_headers
    
    # Convertir la columna 'SKU' a string para evitar problemas con los valores numéricos
    df['SKU'] = df['SKU'].astype(str)
    
    # Convertir las columnas de pallets a flotantes y manejar las fechas como flotantes
    def convert_date_to_float(date_value):
        if isinstance(date_value, pd.Timestamp):
            # Extraer el día del mes y dividirlo por 100
            return date_value.day + (date_value.month / 100)
        return date_value  # Si no es una fecha, devolver el valor original

    # Aplicar la conversión a las columnas correspondientes
    df['1 - 9 pallets (DL/LB)'] = df['1 - 9 pallets (DL/LB)'].apply(convert_date_to_float)
    df['10 - 19 pallets (DL/LB)'] = df['10 - 19 pallets (DL/LB)'].apply(convert_date_to_float)
    df['+ 20 pallets (DL/LB)'] = df['+ 20 pallets (DL/LB)'].apply(convert_date_to_float)
    
    # Eliminar las columnas "Primal" y "NAM"
    df = df.drop(columns=['Primal', 'NAM'], errors='ignore')
    
    # Crear un multiselect para buscar por SKUs
    selected_skus = st.multiselect(
        "Selecciona SKUs", 
        options=df['SKU'].unique(), 
        default=default_skus
    )
    
    # Filtrar los datos según los SKUs seleccionados
    if selected_skus:
        filtered_content = df[df['SKU'].isin(selected_skus)]
    else:
        filtered_content = df

    # Mostrar la tabla filtrada
    st.write(filtered_content)

else:
    st.warning("Por favor, sube un archivo de Excel para continuar.")
