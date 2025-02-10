"""Copilot: 
    In folder tryouts, module try1.py 
    read file "IR Report Cash Flow_2024.xlsm" from the Data folder; 
    show a numbered list of all tabs in this sheet. 
    Read the tab named "SF1-AT", show the list of column names and 
    show the first 10 rows for the 6 rightmost columns on this tab"""
import os
from datetime import datetime
import pandas as pd
import streamlit as st


# Extract the username
username = os.getlogin()

# Extract the current timestamp
current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# File uploader to select the input file
uploaded_file = st.file_uploader("Choose an Excel file to upload")

if uploaded_file is not None:
    # Extract the absolute path to the input file
    # file_path = uploaded_file.name
    file_dir = os.path.abspath(uploaded_file.name)
    file_dir = os.path.dirname(file_dir)
    file_dir = os.path.join(file_dir, "data")

    # st.write(f"Input File Path: {file_path}")
    st.write(f"Input File Dir: {file_dir}")

    # Load the Excel file
    xls = pd.ExcelFile(uploaded_file)

    # Create an array with the specified columns
    data_array = []

    # Iterate through each tab in the sheet where the tab name starts with "SF"
    for sheet_name in xls.sheet_names:
        if sheet_name.startswith("SF"):
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name).convert_dtypes()

            # Add the first row with 'BM' data type
            data_array.append([
                username, current_timestamp, uploaded_file.name, sheet_name, 'BM',
                df.iloc[2, 127].strftime('%Y-%m-%d'), str(df.iloc[2, 128]), df.iloc[2, 129]
            ])

            # Add rows based on the conditions
            for index, row in df.iterrows():
                if index < 3:
                    continue
                else:
                    effective_date_po = str(row.iloc[124]).strip()
                    effective_date_bm = str(row.iloc[127]).strip()
                    try:
                        effective_date_po= datetime.strptime(effective_date_po, '%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        # print("\nError in line:", index, ",", row.iloc[124],".")
                        break
                    else:
                        # print("\nrow[124]:",
                        # datetime.strptime(row.iloc[124], '%Y-%m-%d %H:%M:%S'),".")
                        data_array.append([
                            username, current_timestamp, uploaded_file.name, sheet_name, 'PO',
                            effective_date_po.strftime('%Y-%m-%d'), str(row.iloc[125]),
                            row.iloc[126]
                        ])
                    try:
                        effective_date_bm= datetime.strptime(effective_date_bm, '%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        # print("\nError", row.iloc[127],".")
                        pass
                    else:
                        data_array.append([
                            username, current_timestamp, uploaded_file.name, sheet_name, 'BM',
                            effective_date_bm.strftime('%Y-%m-%d'), str(row.iloc[128]),
                            row.iloc[129]
                        ])

    # Display the array
    # for row in data_array:
    #     print(row)

    # Convert the array to a DataFrame
    columns = ['upload_user', 'upload_timestamp', 'upload_filepath', 'sheet_name', 'data_type',
            'effective_date', 'amount', 'currency']
    df_normalized = pd.DataFrame(data_array, columns=columns)

    # Write the DataFrame to an Excel file
    output_file_path = os.path.join(file_dir, 'NormalizedData.xlsx')
    df_normalized.to_excel(output_file_path, index=False)

    st.write(f"Data has been written to {output_file_path}")
else:
    st.write("No file selected. Please upload an Excel file.")
