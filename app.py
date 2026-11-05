import os
import json
import random
import time
import html
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image
from geopy.geocoders import Nominatim
import streamlit as st

# Page configuration 
try:
    logo_img = Image.open("logo.jpeg")
except Exception:
    logo_img = "🌌"
st.set_page_config(
    page_title="OceaNova Action", 
    page_icon=logo_img, 
    layout="wide"
)

# Importing security modules from your src/ directory
from src.ingestion_satellite import fetch_satellite_metadata
from src.health_risk_calculation import calculate_one_health_indices

# Css style applied
st.markdown("""
    <style>
        h1, h2, h3 { 
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
        }
        div[data-testid="stMetric"] { 
            background-color: rgba(128, 128, 128, 0.08) !important; 
            padding: 15px; 
            border-radius: 10px; 
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-left: 5px solid #00B4D8 !important; 
        }
        div[data-testid="stForm"] { 
            border: 1px solid rgba(128, 128, 128, 0.25); 
            background-color: transparent !important;
            border-radius: 10px; 
        }
    </style>
""", unsafe_allow_html=True)


# Translation French/English
LANG_DICT = {
    "FR": {
        "title": "OceaNova Action — One Health Predictive Dashboard",
        "subtitle": "Infrastructure DeepTech d'Alerte Précoce pour les Risques de Microplastiques et la Protection Maternelle",
        "lang_select": "Choisir la langue / Select Language",
        "monitored_hotspots": "Hotspots Surveillés",
        "mean_global": "Indice de Risque Global Moyen",
        "mean_maternal": "Indice Endocrinien Maternel Moyen",
        "scope": "Zone d'analyse",
        "toxicity_level": "Niveau de toxicité de l'écosystème",
        "hazard_level": "Niveau de danger reproductif",
        "sidebar_title": "Pipeline de Science Citoyenne",
        "input_location": "Nom du cours d'eau / Repère local (ex: Marché de Mouanko)",
        "input_country": "Pays",
        "input_eco": "Type d'Écosystème",
        "btn_add": "Localiser et Analyser",
        "btn_delete": "Supprimer le dernier point",
        "alert_success": "Lieu localisé avec succès par l'IA !",
        "alert_error": "Impossible de localiser ce lieu. Veuillez préciser (ex: Mouanko, Cameroun)",
        "map_title": "Cartographie en Direct des Risques Microplastiques",
        "chart_title": "Évolution Temporelle de l'Accumulation Toxique",
        "all": "Tous les pays"
    },
    "EN": {
        "title": "OceaNova Action — One Health Predictive Dashboard",
        "subtitle": "Early-Warning DeepTech Infrastructure for Riverine Microplastic Risks & Maternal Health Protection",
        "lang_select": "Choisir la langue / Select Language",
        "monitored_hotspots": "Monitored Hotspots",
        "mean_global": "Mean Global Risk Index",
        "mean_maternal": "Mean Maternal Endocrine Index",
        "scope": "Scope",
        "toxicity_level": "Ecosystem Toxicity Level",
        "hazard_level": "Reproductive Hazard Level",
        "sidebar_title": "Citizen Science Input Pipeline",
        "input_location": "River Name / Local Landmark (e.g., Mouanko Market)",
        "input_country": "Country",
        "input_eco": "Ecosystem Type",
        "btn_add": "Locate & Analyze",
        "btn_delete": "Delete Last Hotspot",
        "alert_success": "Location successfully mapped by AI!",
        "alert_error": "Location not found. Please be more specific (e.g., Mouanko, Cameroon)",
        "map_title": "Live Microplastic Risk Mapping",
        "chart_title": "Temporal Evolution of Toxic Bioaccumulation",
        "all": "All Countries"
    }
}
# Language selection at the very top of the sidebar
lang_choice = st.sidebar.selectbox(LANG_DICT["FR"]["lang_select"], ["Français 🇫🇷", "English 🇬🇧"])
L = LANG_DICT["FR"] if "Français" in lang_choice else LANG_DICT["EN"]
st.title(L["title"])
st.markdown(f"**{L['subtitle']}** | *Founder & CEO: Rosanne Masugue Ngangoumoun | Millennium Fellow 2026*")


# Initialization of session state memory
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    # Initial default data
    st.session_state.hotspots = [
        {"name": "Nyabarongo River", "country": "Rwanda", "ecosystem": "River", "latitude": -1.97, "longitude": 30.10, "global_risk": 75, "maternal_risk": 81},
        {"name": "Sanaga River", "country": "Cameroun", "ecosystem": "River", "latitude": 4.20, "longitude": 10.50, "global_risk": 72, "maternal_risk": 78},
        {"name": "Wouri Estuary", "country": "Cameroun", "ecosystem": "Estuary", "latitude": 4.01, "longitude": 9.67, "global_risk": 80, "maternal_risk": 85}
    ]
# Sidebar input forms
st.sidebar.header(L["sidebar_title"])

with st.sidebar.form("citizen_input_form"):
    location_input = st.text_input(L["input_location"], value="")
    country_input = st.selectbox(L["input_country"], ["Cameroun", "Rwanda", "Nigeria", "RDC", "Burundi", "Kenya", "Ghana", "Chad", "Gabon"])
    eco_input = st.selectbox(L["input_eco"], ["River", "Lake", "Estuary", "Oceans and Seas", "Mangrove Swamps", "Wetlands", "Coral Reefs"])
    
    submitted = st.form_submit_button(L["btn_add"])
    
# Delete button outside the form for immediate action    
if st.sidebar.button(L["btn_delete"]) and len(st.session_state.hotspots) > 0:
    st.session_state.hotspots.pop()
    st.rerun()

# Geocoding logic and independent calculations
if submitted and location_input:
    geolocator = Nominatim(user_agent="oceanova_analytics_agent")
    try:
        search_query = f"{location_input}, {country_input}"
        location = geolocator.geocode(search_query, timeout=10)
        
        if location:
            simulated_fdi = random.uniform(0.4, 0.9)
            simulated_stagnation = random.randint(40, 95)
            simulated_reports = random.randint(30, 85)
            
            risk_results = calculate_one_health_indices(simulated_fdi, simulated_stagnation, simulated_reports)
            
            new_point = {
                "name": location_input,
                "country": country_input,
                "ecosystem": eco_input,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "global_risk": risk_results["global_risk_index"],
                "maternal_risk": risk_results["maternal_endocrine_index"]
            }
            st.session_state.hotspots.append(new_point)
            st.sidebar.success(L["alert_success"])
            st.rerun()
        else:
            st.sidebar.error(L["alert_error"])
    except Exception:
        st.sidebar.error(L["alert_error"])

# Filter and main interface
country_filter = st.selectbox(f"{L['scope']}", [L["all"]] + list(set([h["country"] for h in st.session_state.hotspots])))

# Applying filtering    
filtered_hotspots = [
    h for h in st.session_state.hotspots 
    if country_filter == L["all"] or h["country"] == country_filter
]
# Dynamic calculation of metrics
if filtered_hotspots:
    total_hotspots = len(filtered_hotspots)
    avg_global = int(sum([h["global_risk"] for h in filtered_hotspots]) / total_hotspots)
    avg_maternal = int(sum([h["maternal_risk"] for h in filtered_hotspots]) / total_hotspots)
else:
    total_hotspots, avg_global, avg_maternal = 0, 0, 0
    
# Displaying metrics
col1, col2, col3 = st.columns(3)

col1.metric(L["monitored_hotspots"], total_hotspots, delta=f"Scope: {country_filter}")
col2.metric(L["mean_global"], f"{avg_global} / 100", delta=L["toxicity_level"], delta_color="inverse")
col3.metric(L["mean_maternal"], f"{avg_maternal} / 100", delta=L["hazard_level"], delta_color="inverse")

st.write("---")

# Control and display of the folium card
st.subheader(f"{L['map_title']}")
if filtered_hotspots:
    # Safe centering on the first item [0] in the filtered list
    m = folium.Map(location=[filtered_hotspots[0]["latitude"], filtered_hotspots[0]["longitude"]], zoom_start=5, control_scale=True)
    
    for h in filtered_hotspots:
        popup_text = f"<b>{h['name']}</b><br>Global Risk: {h['global_risk']}/100<br>Maternal Index: {h['maternal_risk']}/100"
        folium.Marker(
            location=[h["latitude"], h["longitude"]],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color="red" if h["maternal_risk"] > 70 else "orange", icon="info-sign")
        ).add_to(m)
        
    st_folium(m, width=1300, height=450, key="oceanova_map")
else:
    st.info("No active hotspots to map for this scope.")

st.write("---")

# Summary time-series chart
st.subheader(f"{L['chart_title']}")
if filtered_hotspots:
    chart_data = pd.DataFrame({
        "Timeline": ["2024", "2025", "Nov 2026"],
        "Global Risk Trend": [avg_global * 0.7, avg_global * 0.85, avg_global],
        "Maternal Endocrine Trend": [avg_maternal * 0.65, avg_maternal * 0.8, avg_maternal],
    }).set_index("Timeline")
    st.line_chart(chart_data)
else:
    st.info("No temporal data available.")
