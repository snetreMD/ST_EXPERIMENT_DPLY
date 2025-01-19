"""Copilot: write python code to 
    select a csv file with Streamlit,
    read it with pandas, 
    add the user's OS name, current system timestamp and filename to each row and
    write the records into a snowflake table;
    edited the generated code to use write_pandas instead of to_sql;
    also isolated the snowflake connection password into the secrets.toml."""
from datetime import datetime
import getpass
import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# Streamlit file uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Fetch the current system timestamp
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Fetch the name of the user running the code
    user_name = getpass.getuser()

    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file, sep=';').convert_dtypes()

    # Add timestamp, filename and user name to the DataFrame
    df['timestamp'] = current_timestamp
    df['filename'] = uploaded_file.name
    df['user_name'] = user_name

    # Add extra columns to the DataFrame
    df['extra_text'] = 'bla bla bla'
    df['extra_num'] = 1234

    # Display the DataFrame
    st.write(df)

    # Snowflake connection parameters
    conn_params = {
        'user': 'DANNY',
        'password': st.secrets["snowflake"]["password"],
        'account': 'nwtrvxw-yp81693',
        'warehouse': 'COMPUTE_WH',
        'database': 'TESTS',
        'schema': 'UPLOADS'
    }

    # Connect to Snowflake
    conn = snowflake.connector.connect(**conn_params)

    # Write the DataFrame to a Snowflake table
    TABLE_NAME = 'UPLOADED'
    write_pandas(conn, df, TABLE_NAME, auto_create_table=True)
    # df.to_sql(TABLE_NAME, conn, if_exists='append', index=False)

    st.success(f"Data successfully written to {TABLE_NAME} table in Snowflake")

    # Close the connection
    conn.close()
