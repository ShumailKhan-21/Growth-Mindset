import streamlit as st
import pandas as pd
import os
from io import BytesIO

#App set up

st.set_page_config(page_title="Data Morph", layout="wide")
st.title("Data Morph")
st.write("🚀 Welcome to DataMorph! Convert between CSV & Excel, clean messy data, and visualize insights effortlessly.")
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=['csv','xlsx'],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext= os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported dile type: {file_ext}")
            continue 

        #information of file   
        st.write(f"**File name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        # Show 5 rows of our Data Frame
        st.write("Preview the head of Data Frame")
        st.dataframe(df.head())

        # Options for Cleaning the Data

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Removes Duplicate from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

                           

        # Choose Specific Columns to Keep or Convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columnns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #Creating Visualization for my data

        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion of file types

        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV","Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index= False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)  

            #Download Option

            st.download_button(
                label=f" Download {file.name} as {conversion_type}",
                data = buffer ,
                file_name = file_name ,
                mime= mime_type

            )  

st.success("Files Processed!")



