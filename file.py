import streamlit as st
import pandas as pd
import os
from io import BytesIO  # Import BytesIO

st.set_page_config(page_title="FILE CONVERTER", layout="wide")
st.title("FILE CONVERTER AND CLEANER:")
st.write("Submit your CSV and Excel files, sanitize the data, and reformat accordingly.")

files = st.file_uploader("Drop your CSV and Excel files here", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
        st.write("Preview....")
        st.dataframe(df.head())

        # Data cleaning
        st.subheader("Data cleaning...")
        if st.checkbox(f"Clean data from {file.name}"):
            col1, col2 = st.columns(2)
            # For duplicates removal
            with col1:
                if st.button(f"Remove duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("DUPLICATES REMOVED...")

            # For missing data
            with col2:
                if st.button(f"Fill the missing values: {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled with mean.")

        # Select columns to convert
        st.subheader("Select columns to convert.")
        columns = st.multiselect(f"Choose columns from {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("Data Visualization:")
        if st.checkbox(f'Show Visualization from {file.name}'):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion options
        st.subheader("Conversion Options:")
        conversion_type = st.radio(f'Convert {file.name} to:', ["csv", "excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

            st.success("Your file(s) have been processed successfully.")
