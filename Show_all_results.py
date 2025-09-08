import streamlit as st
from PIL import Image
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
import requests
import os

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

# --- 3️⃣ Define zip files for each category ---
zip_configs = {
    "Motor": {"zip_name": "Motor_images.zip", "from_github": True},
    "Power": {"zip_name": "Power_images.zip", "from_github": True},
    "Battery": {"zip_name": "Battery_images.zip", "from_github": True},
    "Resource": {"zip_name": "Resource_images/Resource_images.zip", "from_github": False},  # LFS, use local
    "Mining": {"zip_name": "Mining_images.zip", "from_github": False}       # LFS, use local
}

base_url = "https://raw.githubusercontent.com/Pelotte/App_IAM_Metal_Demand_Opti_Tech_MS/main"

# --- 4️⃣ Load and display images ---
for title, cfg in zip_configs.items():
    st.subheader(f"{title} Images")
    zip_file = None

    try:
        if cfg["from_github"]:
            # Download small zips from GitHub
            zip_url = f"{base_url}/{cfg['zip_name']}"
            r = requests.get(zip_url)
            r.raise_for_status()
            zip_file = ZipFile(BytesIO(r.content))
        else:
            # Resource and Mining: use local LFS files
            if not os.path.exists(cfg['zip_name']):
                st.warning(f"{cfg['zip_name']} not found locally. Make sure to run 'git lfs pull' and include it in the repo.")
                continue
            zip_file = ZipFile(cfg['zip_name'])
    except Exception as e:
        st.warning(f"Cannot open {cfg['zip_name']}: {e}")
        continue

    all_files = zip_file.namelist()
    expected_file_suffix = f"Fig_{title}Comparison_{model} - {scenario}.png"

    # Search for the file in the zip regardless of folder structure
    found_file = None
    for f in all_files:
        if f.replace("\\","/").endswith(expected_file_suffix):  # handles Windows vs Unix slashes
            found_file = f
            break

    if found_file:
        with zip_file.open(found_file) as file:
            image = Image.open(file)
            st.image(image, caption=f"{model} - {scenario}", use_container_width=True)
    else:
        st.warning(f"No image found in {cfg['zip_name']} for {model} - {scenario}")
