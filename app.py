import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os
import pandas as pd
import random

# Streamlit page configuration
st.set_page_config(page_title="OceaNova Action MVP", page_icon="🌍", layout="wide")
st.title("🌍 OceaNova Action — One Health Predictive Dashboard")
st.markdown("### Early-Warning System for Riverine Microplastic Risks & Maternal Health Protection")

# Path to the GeoJSON file
geojson_path = "data/points_impact_afrique.geojson"

# --- SIDEBAR & FILTERING / CITIZEN SCIENCE SYSTEM ---
st.sidebar.image("https://icons8.com", width=80)
st.sidebar.header("System Controls")
st.sidebar.markdown("**Founder & CEO:** Rosanne Masugue Ngangoumoun")
st.sidebar.markdown("**Status:** Active Development")

# --- SECTION 1: INTERACTIVE MAP FILTERS ---
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filter Trajectories")

# Options par défaut pour les filtres
country_filter = st.sidebar.selectbox("Filter by Country", ["All Countries", "Cameroon", "Rwanda", "Nigeria", "Ghana", "DR Congo", "Kenya"])
waterbody_filter = st.sidebar.selectbox("Filter by Waterbody Type", ["All Types", "River", "Lake", "Ocean/Beach", "Stream/Ditch"])

# --- SECTION 2: CITIZEN SCIENCE FORM ---
st.sidebar.markdown("---")
st.sidebar.subheader("👥 Citizen Science Reporting")
st.sidebar.info("Artisanal fishers and community health workers can report localized plastic pollution anomalies below.")

with st.sidebar.form(key="citizen_report_form", clear_on_submit=True):
    location_name = st.text_input("Waterway / Location Name", placeholder="e.g., Sanaga River, Mouanko")
    new_country = st.selectbox("Country Location", ["Cameroon", "Rwanda", "Nigeria", "Ghana", "DR Congo", "Kenya"])
    new_waterbody_type = st.selectbox("Waterbody Type Classification", ["River", "Lake", "Ocean/Beach", "Stream/Ditch"])
    pollution_density = st.slider("Visual Plastic Density (Field Observation)", 0, 100, 50)
    stagnation_observed = st.checkbox("Water stagnation or drainage blockage observed?")
    submit_button = st.form_submit_button(label=" Submit Field Report")

#  Processing the Citizen report (writing to the GeoJSON)
if submit_button and location_name:
    if os.path.exists(geojson_path):
        with open(geojson_path, "r") as f:
            geojson_data = json.load(f)
        stagnation_factor = 1.4 if stagnation_observed else 1.0
        calculated_risk = min(int(pollution_density * stagnation_factor), 100)
        if calculated_risk > 80:
            hazard_level = "Critical - Endocrine Disruptor & Toxin Bioaccumulation Alert"
        elif calculated_risk > 50:
            hazard_level = "Moderate - Increased Monitoring Required"
        else:
            hazard_level = "Low - Stable Baseline"
        base_coords = {
            "Cameroon": [4.02, 9.68], "Rwanda": [-1.97, 30.04], "Nigeria": [6.45, 3.39],
            "Ghana": [5.55, -0.2], "DR Congo": [-4.32, 15.31], "Kenya": [-1.28, 36.82]
        }
        lat = base_coords[new_country][0] + random.uniform(-0.3, 0.3)
        lon = base_coords[new_country][1] + random.uniform(-0.3, 0.3)
        new_feature = {
            "type": "Feature",
            "properties": {
                "location_name": location_name,
                "country": new_country,
                "waterbody_type": new_waterbody_type,
                "risk_index": calculated_risk,
                "maternal_health_hazard": hazard_level,
                "community_status": "Citizen Verified - Action Plan Initiated"
            },
            "geometry": { "type": "Point", "coordinates": [lon, lat] }
        }
        geojson_data["features"].append(new_feature)
        with open(geojson_path, "w") as f:
            json.dump(geojson_data, f, indent=2)
        st.sidebar.success(f"🎉 Report for '{location_name}' integrated! Refreshing maps...")
        st.rerun()

# --- DASHBOARD PROCESSING & FILTER LOGIC ---
if os.path.exists(geojson_path):
    with open(geojson_path, "r") as f:
        raw_data = json.load(f)
    
    # Dynamic filtering of the list of points based on user choices
    filtered_features = []
    for feature in raw_data["features"]:
        props = feature["properties"]
        
        # Countries condition
        match_country = (country_filter == "All Countries") or (props.get("country") == country_filter)
        # Environment Type Condition
        match_type = (waterbody_filter == "All Types") or (props.get("waterbody_type") == waterbody_filter)
        if match_country and match_type:
            filtered_features.append(feature)

    # --- SECTION 3: 100% DYNAMIC METRICS ---
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    # Métrique 1: Total des hotspots filtrés
    col1.metric("Monitored Hotspots", len(filtered_features), f"Selected: {country_filter}")
    
    # Metric 2: Maximum risk index among filtered items
    if filtered_features:
        max_risk = max([f["properties"]["risk_index"] for f in filtered_features])
        max_loc = next(f["properties"]["location_name"] for f in filtered_features if f["properties"]["risk_index"] == max_risk)
        col2.metric("Highest Risk Index", f"{max_risk}/100", f"Location: {max_loc}", delta_color="inverse")
    else:
        col2.metric("Highest Risk Index", "N/A", "No sites match filters")
        
    # Metric 3: Community Stakeholder Estimator
    total_fishers = sum([15 for _ in filtered_features]) + 150
    col3.metric("Active Field Responders", f"{total_fishers} Fishers", "Community Network Status")

    st.markdown("---")
    st.subheader("📍 Live Microplastic Risk Mapping (One Health Trajectory)")

    # Map initialization centered dynamically according to selection
    map_center = [1.0, 20.0]
    if country_filter != "All Countries" and filtered_features:
        # Center on the first point found for the selected country
        first_coords = filtered_features[0]["geometry"]["coordinates"]
        map_center = [first_coords[1], first_coords[0]]

    m = folium.Map(location=map_center, zoom_start=4 if country_filter == "All Countries" else 7, tiles=None)

    # Basemap layers
    folium.TileLayer(tiles="OpenStreetMap", name="Plan OpenStreetMap", overlay=False, control=True).add_to(m)
    nasa_url = "https://nasa.gov{z}/{y}/{x}.jpg"
    folium.TileLayer(tiles=nasa_url, attr='&copy; NASA EOSDIS GIBS', name="Images Satellites (NASA VIIRS)", overlay=False, control=True).add_to(m)

    # Exclusive display of filtered markers
    for feature in filtered_features:
        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]
        lat, lon = coords[1], coords[0]
        if props["risk_index"] > 80:
            color, badge_color = "red", "#d9534f"
        elif props["risk_index"] > 60:
            color, badge_color = "orange", "#f0ad4e"
        else:
            color, badge_color = "blue", "#0275d8"
        water_type = props.get("waterbody_type", "River")
        icon_name = "tint" if water_type == "Ocean/Beach" else "cloud" if water_type == "Lake" else "leaf" if water_type == "Stream/Ditch" else "exclamation-sign"
        popup_text = f"""
        <div style='font-family: "Segoe UI", Arial, sans-serif; width: 240px; padding: 5px;'>
            <h4 style='margin: 0 0 4px 0; color: #1a2a3a; font-size: 16px;'>{props['location_name']} ({props.get('country', '')})</h4>
            <div style='margin-bottom: 8px;'>
                <span style='background-color: {badge_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;'>
                    {water_type} — Risque : {props['risk_index']}/100
                </span>
            </div>
            <table style='width: 100%; font-size: 12px; border-collapse: collapse; line-height: 1.6;'>
                <tr>
                    <td style='padding: 3px 0; color: #666;'>⚠️ Maternal Danger :</td>
                    <td style='padding: 3px 0; font-weight: bold; color: #d9534f;'>{props['maternal_health_hazard']}</td>
                </tr>
                <tr>
                    <td style='padding: 3px 0; color: #666;'>👥 Community :</td>
                    <td style='padding: 3px 0; font-weight: bold; color: #2e7d32;'>{props['community_status']}</td>
                </tr>
            </table>
        </div>
        """
        folium.Marker(location=[lat, lon], popup=folium.Popup(popup_text, max_width=280), icon=folium.Icon(color=color, icon=icon_name)).add_to(m)

    folium.LayerControl(position="topright", collapsed=False).add_to(m)
    st_folium(m, width=1100, height=500)

    # --- COMPARATIVE TEMPORAL GRAPH ---
    st.markdown("---")
    st.subheader("📊 Évolution Temporelle des Microplastiques (2024 - 2026)")
    dates = pd.date_range(start="2024-01-01", end="2026-10-01", freq="ME")
    random.seed(42)
    wouri_data = [50 + (i * 1.5) + random.uniform(-5, 5) for i in range(len(dates))]
    rwanda_data = [35 + (i * 0.9) + random.uniform(-4, 4) for i in range(len(dates))]
    
    chart_data = pd.DataFrame({"Mois": dates, "Fleuve Wouri (Cameroun)": wouri_data, "Lac Kivu / Ruzizi (Rwanda)": rwanda_data}).set_index("Mois")
    st.line_chart(chart_data, height=350, use_container_width=True)
    st.caption("Simulated data based on historical Landsat-8 and Sentinel-2 imagery trends.")

else:
    st.error(f"GeoJSON data file not found at {geojson_path}.")
