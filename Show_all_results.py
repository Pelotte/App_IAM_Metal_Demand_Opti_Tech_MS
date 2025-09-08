import streamlit as st
from PIL import Image
import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile

# App title
st.title("Visualize the results for a specific model and scenario")

# --- 1️⃣ Load the Excel study scope from GitHub ---
excel_url = "https://raw.githubusercontent.com/Pelotte/App_IAM_Metal_Demand_Opti_Tech_MS/main/Scope of the study.xlsx"
r = requests.get(excel_url)
r.raise_for_status()
with BytesIO(r.content) as file:
    with pd.ExcelFile(file, engine="openpyxl") as xls:
        listModels = pd.read_excel(xls, 'model', index_col=0).squeeze().tolist()
        listScenarios = pd.read_excel(xls, 'scenario', index_col=0).squeeze().tolist()

# --- 2️⃣ Select model and scenario ---
model = st.selectbox("Choose a model:", listModels)
scenario = st.selectbox("Choose an SSP scenario:", listScenarios)

# --- 3️⃣ Load images zip from GitHub ---
zip_url = "https://github.com/Pelotte/App_IAM_Metal_Demand_Opti_Tech_MS/raw/main/Images.zip"
r = requests.get(zip_url)
r.raise_for_status()
zip_file = ZipFile(BytesIO(r.content))

# List all files in the zip
all_files = zip_file.namelist()

# --- 4️⃣ Define the images configuration ---
image_configs = {
    "Comparing cumulated demand to resources and reserves": {
        "folder": "Resource_images",
        "filename": f"Fig_Resource_{model} - {scenario}.png"
    },
    "Annual demands and mining capacities": {
        "folder": "Mining_images",
        "filename": f"Fig_Mining_{model} - {scenario}.png"
    },
    "Power plant market shares": {
        "folder": "Power_images",
        "filename": f"Fig_PowerComparison_{model} - {scenario}.png"
    },
    "Electric vehicle motor market shares": {
        "folder": "Motor_images",
        "filename": f"Fig_MotorComparison_{model} - {scenario}.png"
    },
    "Electric vehicle battery market shares": {
        "folder": "Battery_images",
        "filename": f"Fig_BatteryComparison_{model} - {scenario}.png"
    }
}

# --- 5️⃣ Loop over images and display ---
for title, cfg in image_configs.items():
    st.subheader(title)
    image_path = f"{cfg['folder']}/{cfg['filename']}"
    
    if image_path in all_files:
        with zip_file.open(image_path) as file:
            image = Image.open(file)
            st.image(image, caption=f"{model} - {scenario}", use_column_width=True)
    else:
        st.warning(f"No existing figure in {title} for {model} - {scenario}")
