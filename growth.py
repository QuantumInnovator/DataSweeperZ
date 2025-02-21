import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")  

st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description with icons
st.markdown("# 🚀 Data Sterling Integrator")
st.write("🔄 Transform your files between CSV and Excel formats with built-in data cleaning and validation tools.")

# File uploader
upload_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # File details
        st.markdown(f"## 📑 Preview of `{file.name}`")
        st.dataframe(df.head())

        # Data Cleaning
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"✨ Clean the Data for `{file.name}`"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates from `{file.name}`"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicate Removed")

            with col2:
                if st.button(f"🩹 Fill Missing Values for `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled")

            # Column selection
            st.subheader("🎛️ Select Columns to Keep")
            columns = st.multiselect(f"📌 Choose columns for `{file.name}`", df.columns, default=df.columns)
            df = df[columns]

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"📈 Show visualization for `{file.name}`"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # Conversion Options
            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"🔀 Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

            if st.button(f"💾 Convert `{file.name}`"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)

                st.download_button(
                    label=f"⬇️ Download `{file.name}` as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

        st.success(f"🎉 `{file.name}` processed successfully!")