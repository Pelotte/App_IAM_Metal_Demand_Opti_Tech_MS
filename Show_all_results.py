import streamlit as st
from PIL import Image
import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile

# --- 1️⃣ Load the Excel study scope ---
excel_url = "https://raw.githubusercontent.com/Pelotte/App_IAM_Metal_Demand_Opti_Tech_MS/main/Scope%20of%20the%20study.xlsx"
r = requests.get(excel_url)
r.raise_for_status()
with BytesIO(r.content) as file:
    with pd.ExcelFile(file, engine="openpyxl") as xls:
        listModels = pd.read_excel(xls, 'model', index_col=0).squeeze().tolist()
        listScenarios = pd.read_excel(xls, 'scenario', index_col=0).squeeze().tolist()

# --- 2️⃣ Select model and scenario ---
model = st.selectbox("Choose a model:", listModels)
scenario = st.selectbox("Choose an SSP scenario:", listScenarios)

# --- 3️⃣ Define zip files for each image category ---
zip_configs = {
    "Motor": "Motor_images.zip",
    "Power": "Power": "Power_images.zip",
    "Battery": "Battery_images.zip"
}

# Base URL raw GitHub
base_url = "https://raw.githubusercontent.com/Pelotte/App_IAM_Metal_Demand_Opti_Tech_MS/main"

# --- 4️⃣ Load and display images ---
for title, zip_name in zip_configs.items():
    st.subheader(f"{title} Images")
    zip_url = f"{base_url}/{zip_name}"
    
    r = requests.get(zip_url)
    if r.status_code != 200:
        st.warning(f"Cannot download {zip_name}")
        continue
    
    zip_file = ZipFile(BytesIO(r.content))
    all_files = zip_file.namelist()
    
    # Construct expected filename based on model and scenario
    expected_filename = f"{title}_images/Fig_{title}Comparison_{model} - {scenario}.png"
    
    if expected_filename in all_files:
        with zip_file.open(expected_filename) as file:
            image = Image.open(file)
            st.image(image, caption=f"{model} - {scenario}", use_column_width=True)
    else:
        st.warning(f"No image found in {zip_name} for {model} - {scenario}")
