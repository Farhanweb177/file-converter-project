import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter")
st.write("Upload CSV or Excel file, clean data and convert format")

file = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if file:
    for files in file:
        ext = files.name.split(".")[-1]
        df = pd.read_csv(files) if ext == "csv" else pd.read_excel(files)

        st.subheader(f"{files.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove duplicates - {files.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates removed")
            st.dataframe(df.head())

        if st.checkbox(f"Fill missing values - {files.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing values filled with mean")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select columns - {files.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show chart - {files.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {files.name} to", ["csv", "Excel"], key=files.name)

        if st.button(f"Download {files.name} to {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = files.name.rsplit(".", 1)[0] + ".csv"
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = files.name.rsplit(".", 1)[0] + ".xlsx"

            output.seek(0)
            st.download_button("Download file", file_name=new_name, data=output, mime=mime)

        st.success("Processing complete!")
