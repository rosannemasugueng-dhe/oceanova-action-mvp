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
st.caption(f"{L['subtitle']} | Founder & CEO: Rosanne Masugue Ngangoumoun")

# Initialization of session state memory
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    try:
        with open("data/points_impact_africa.geojson", "r", encoding="utf-8") as f:
            geo_data = json.load(f)
        st.session_state.hotspots = [
            {
                "name": ft["properties"].get("location_name", ft["properties"].get("name", "Unknown River")),
                "country": ft["properties"].get("country", "Unknown"),
                "ecosystem": ft["properties"].get("waterbody_type", ft["properties"].get("ecosystem", "River")),
                "latitude": ft["geometry"]["coordinates"][1],
                "longitude": ft["geometry"]["coordinates"][0],
                "global_risk": ft["properties"].get("global_risk_index", 50),
                "maternal_risk": ft["properties"].get("maternal_endocrine_index", 50),
            }
            for ft in geo_data["features"]
        ]
    except Exception:
        st.session_state.hotspots = []


st.sidebar.header(L["sidebar_title"])
with st.sidebar.form("citizen_input_form"):
    location_input = st.text_input(L["input_location"], value="")
    country_input = st.selectbox(L["input_country"],
        ["Cameroon", "Rwanda", "Nigeria", "Ghana", "DR Congo", "Kenya"])
    eco_input = st.selectbox(L["input_eco"], ["River", "Lake", "Estuary"])
    submitted = st.form_submit_button(L["btn_add"])
if st.sidebar.button(L["btn_delete"]) and len(st.session_state.hotspots) > 0:
    st.session_state.hotspots.pop()
    st.rerun()
if submitted and location_input:
    geolocator = Nominatim(user_agent="oceanova_analytics_agent")
    try:
        location = geolocator.geocode(f"{location_input}, {country_input}", timeout=10)
        if location:
            risk = calculate_one_health_indices(
                random.uniform(0.4, 0.9), random.randint(40, 95), random.randint(30, 85)
            )
            st.session_state.hotspots.append({
                "name": location_input, "country": country_input, "ecosystem": eco_input,
                "latitude": location.latitude, "longitude": location.longitude,
                "global_risk": risk["global_risk_index"],
                "maternal_risk": risk["maternal_endocrine_index"],
            })
            st.rerun()
        else:
            st.sidebar.error(L["alert_error"])
    except Exception:
        st.sidebar.error(L["alert_error"])


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
    total_hotspots, avg_global, avg_maternal = 0, 0, 0col1, col2, col3 = st.columns(3)

# Displaying metrics
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
