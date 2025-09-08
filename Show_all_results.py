import streamlit as st
from PIL import Image
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
import requests
import os

# App Title
st.title("Metal bottlenecks along energy transitions call for technology flexibility and sobriety")

# Subtitle
st.subheader("Results for the 110 IAMs scenarios and SSP-RCP under study")

# --- App Introduction ---
st.markdown("""
This app displays additional results linked to the article:

**"Metal bottlenecks along energy transitions call for technology flexibility and sobriety"**  
Submitted by Pénélope Bieuville et al., 2025.

If you encounter any issues, please contact the app owner at [penelope.bieuville@gmail.com](mailto:penelope.bieuville@gmail.com).
""")

# Load the Excel study scope ---
excel_url = "https://raw.githubusercontent.com/Pelotte/App_IAM_Metal_Demand_Opti_Tech_MS/main/Scope%20of%20the%20study.xlsx"
r = requests.get(excel_url)
r.raise_for_status()

with BytesIO(r.content) as file:
    with pd.ExcelFile(file, engine="openpyxl") as xls:
        listModels = pd.read_excel(xls, 'model', index_col=0).squeeze().tolist()
        listScenarios = pd.read_excel(xls, 'scenario', index_col=0).squeeze().tolist()

# Select model and scenario
model = st.selectbox("Choose a model:", listModels)
scenario = st.selectbox("Choose an SSP scenario:", listScenarios)

# Define zip files for each category
zip_configs = {
    "Resource": {"zip_name": "Resource_images.zip", "from_github": False},  # LFS, use local
    "Mining": {"zip_name": "Mining_images.zip", "from_github": False},       # LFS, use local
    "PowerComparison": {"zip_name": "Power_images.zip", "from_github": True},
    "MotorComparison": {"zip_name": "Motor_images.zip", "from_github": True},
    "BatteryComparison": {"zip_name": "Battery_images.zip", "from_github": True}
}

base_url = "https://raw.githubusercontent.com/Pelotte/App_IAM_Metal_Demand_Opti_Tech_MS/main"

# Define legends for each figure type
legends = {
    "Resource": """Global cumulated metal demand from 2020 to 2050 per metal and economic sector aggregates,
compared to estimated reserves and resources. The identified resources are normalized at 1
(=100%) and normalized metal demand and reserves are calculated as a fraction of resources. For
power plants, EVs and the electric grid, the pastel colors represent the initial IAM demands, while
the hatched parts represent a decrease and the darker colors an increase in metal demand because of
the optimization of technological market shares. In grey are the demands that are identical between
both scenarios.""",
    "Mining": """Global yearly metal demand from 2020 to 2050 by economic sector, compared to mining
capacity. For power plant, EV and grid, pastel colors represent initial demand, while the hatched part
represents a decrease and the darker color an increase in metal demand because of the optimization
of technological market shares. Primary mining capacity is represented by an noncontinuous line.
For metals used in EV, mining capacity includes secondary production from the EV sector, with a
division between the one from the initial scenario (red) and the optimization scenario (dark red).""",
"PowerComparison": """Comparison of the market share mix of cumulated installed power capacities required to meet
the power plant demand projected by the chosen model and scenario. On the left, the initial market
share mix based on IMAGE’s power plant mix estimates and the most likely sub-technological market
shares from the literature. On the right, the optimized market shares of power plant sources, designed
to avoid exceeding material constraints. The total installed power capacity varies between the initial
and optimized scenario since the energy output of 1 gigawatt (GW) depends on the capacity factor
of each technology.""",
    "MotorComparison": """Comparison of the market share mix of EVs motors required to meet the light duty vehicle
(LDV) demand projected by the chosen model and scenario, combined with the estimated share
of EVs from the announced pledges IEA scenario. On the left, the initial market share mix based on
the most likely sub-technological market shares from the literature, assuming 100% copper wiring in
motors. On the right, the optimized market shares of engines, designed to avoid exceeding material
constraints, with the potential substitution of copper by aluminum in motor wiring.""",
    "BatteryComparison": """Comparison of the market share mix of batteries in EVs required to meet the light duty
vehicle demand projected by the chosen model and scenario, combined with the estimated share of
EVs from the Announced Pledges IEA Scenario (APS). On the left, the initial market share mix based
on the most likely sub-technological market shares from the literature. On the right, the optimized
market share of batteries, designed to avoid exceeding material constraints."""
}

# Load and display images
for title, cfg in zip_configs.items():
    st.subheader(f"{title} Images")
    zip_file = None

    try:
        if cfg["from_github"]:
            zip_url = f"{base_url}/{cfg['zip_name']}"
            r = requests.get(zip_url)
            r.raise_for_status()
            zip_file = ZipFile(BytesIO(r.content))
        else:
            if not os.path.exists(cfg['zip_name']):
                st.warning(f"{cfg['zip_name']} not found locally.")
                continue
            zip_file = ZipFile(cfg['zip_name'])
    except Exception as e:
        st.warning(f"Cannot open {cfg['zip_name']}: {e}")
        continue

    all_files = zip_file.namelist()
    expected_file_suffix = f"Fig_{title}_{model} - {scenario}.png"

    found_file = None
    for f in all_files:
        if f.replace("\\","/").endswith(expected_file_suffix):
            found_file = f
            break

    if found_file:
        with zip_file.open(found_file) as file:
            image = Image.open(file)
            st.image(image, caption=f"{model} - {scenario}", use_container_width=True)
        # Add legend under the figure
        legend_text = legends.get(title, "")
        if legend_text:
            st.caption(legend_text)
    else:
        st.warning(f"No image found in {cfg['zip_name']} for {model} - {scenario}")

