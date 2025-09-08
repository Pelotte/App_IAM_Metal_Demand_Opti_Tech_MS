import streamlit as st
from PIL import Image
import os
import pandas as pd

# App title
st.title("Visualize the results for a specific model and scenario")

# Base URL for your GitHub repository (raw content)
base_url = "https://raw.githubusercontent.com/Pelotte/App_IAM_Metal_Demand_Opti_Tech_MS/main"

# Load the study scope Excel file directly from GitHub
scope_url = f"{base_url}/Scope of the study.xlsx"
with requests.get(scope_url) as r:
    r.raise_for_status()
    with BytesIO(r.content) as file:
        with pd.ExcelFile(file) as xls:
            listModels = pd.read_excel(xls, 'model', index_col=0).squeeze().tolist()
            listScenarios = pd.read_excel(xls, 'scenario', index_col=0).squeeze().tolist()
        
# Select model and scenario
model = st.selectbox("Choose a model:", listModels)
scenario = st.selectbox("Choose an ssp scenario:", listScenarios)

# Define the figures to load
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

# Loop over figures
for title, cfg in image_configs.items():
    st.subheader(title)
    img_url = f"{base_url}/{cfg['folder']}/{cfg['filename']}"
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=f"{model} - {scenario}", use_container_width=True)
        else:
            st.warning(f"No existing figure in {title} for {model} - {scenario}")
    except Exception as e:
        st.error(f"Error loading image {cfg['filename']}: {e}")



