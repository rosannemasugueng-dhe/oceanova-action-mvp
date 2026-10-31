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

# Information sidebar
st.sidebar.image("https://icons8.com", width=80)
st.sidebar.header("System Controls")
st.sidebar.markdown("**Founder & CEO:** Rosanne Masugue Ngangoumoun")
st.sidebar.markdown("**Status:** Active Development (Simulated Pipeline)")

# Verification and loading of the GeoJSON file
geojson_path = "data/points_impact_afrique.geojson"

if os.path.exists(geojson_path):
    with open(geojson_path, "r") as f:
        data = json.load(f)
    
    # Global metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Monitored Hotspots", len(data["features"]), "Inland Waterways")
    col2.metric("Highest Risk Index", "95/100", "Wouri River, Cameroon", delta_color="inverse")
    col3.metric("Active Field Responders", "150+ Artisanal Fishers", "Rwanda & Cameroon")

    st.markdown("---")
    st.subheader("📍 Live Microplastic Risk Mapping (One Health Trajectory)")

    # Map initialization
    m = folium.Map(location=[1.0, 20.0], zoom_start=4, tiles=None)

  # 1. CARTO VOYAGER BASEMAP LAYER
    carto_url = "https://cartocdn.com{z}/{x}/{y}.png?key=cb1_4yz4_1_6b35e3bbdf97b0cc6d399578"
    carto_attribution = '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors &copy; <a href="https://carto.com">CARTO</a>'
    
    folium.TileLayer(
        tiles=carto_url,
        attr=carto_attribution,
        name="Plan CARTO Voyager",
        overlay=False,
        control=True
    ).add_to(m)

    #2. NASA SATELLITE LAYER (GIBS – VIIRS True Color)
    nasa_url = "https://nasa.gov{z}/{y}/{x}.jpg"
    nasa_attribution = '&copy; <a href="https://nasa.gov">NASA EOSDIS GIBS</a>'

    folium.TileLayer(
        tiles=nasa_url,
        attr=nasa_attribution,
        name="Images Satellites (NASA VIIRS)",
        overlay=False,
        control=True
    ).add_to(m)

    # Adding markers from GeoJSON with ENHANCED INTERACTIVE POPUPS
    for feature in data["features"]:
        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]
        
        lat, lon = coords[1], coords[0]
        
        # Logic for badge and marker colors
        if props["risk_index"] > 80:
            color = "red"
            badge_color = "#d9534f"
        else:
            color = "orange"
            badge_color = "#f0ad4e"
            
        # HTML design of the “Dashboard” style popup
        popup_text = f"""
        <div style='font-family: "Segoe UI", Arial, sans-serif; width: 240px; padding: 5px;'>
            <h4 style='margin: 0 0 4px 0; color: #1a2a3a; font-size: 16px;'>{props['location_name']}</h4>
            <div style='margin-bottom: 8px;'>
                <span style='background-color: {badge_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;'>
                    Risque : {props['risk_index']}/100
                </span>
            </div>
            <table style='width: 100%; font-size: 12px; border-collapse: collapse; line-height: 1.6;'>
                <tr>
                    <td style='padding: 3px 0; color: #666;'>⚠️ Danger Maternel :</td>
                    <td style='padding: 3px 0; font-weight: bold; color: #d9534f;'>{props['maternal_health_hazard']}</td>
                </tr>
                <tr>
                    <td style='padding: 3px 0; color: #666;'>👥 Communauté :</td>
                    <td style='padding: 3px 0; font-weight: bold; color: #2e7d32;'>{props['community_status']}</td>
                </tr>
            </table>
        </div>
        """
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=280),
            icon=folium.Icon(color=color, icon="exclamation-sign" if color=="red" else "info-sign")
        ).add_to(m)

    # Adding the layer selector
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    # Map display
    st_folium(m, width=1100, height=500)

   # --- ADDITION OF THE MICROPLASTICS TEMPORAL GRAPH ---
    st.markdown("---")
    st.subheader("📊 Évolution Temporelle des Microplastiques (2024 - 2026)")
    
    # Creation of simulated pollution data for Cameroon and Rwanda
    dates = pd.date_range(start="2024-01-01", end="2026-10-01", freq="ME")
    
    # Simulation algorithm (upward trend with fluctuations)
    random.seed(42)
    wouri_data = [50 + (i * 1.5) + random.uniform(-5, 5) for i in range(len(dates))]
    rwanda_data = [35 + (i * 0.9) + random.uniform(-4, 4) for i in range(len(dates))]
    
    chart_data = pd.DataFrame({
        "Mois": dates,
        "Fleuve Wouri (Cameroun)": wouri_data,
        "Lac Kivu / Ruzizi (Rwanda)": rwanda_data
    }).set_index("Mois")

    # Displaying the interactive chart via Streamlit
    st.line_chart(chart_data, height=350, use_container_width=True)
    st.caption("Données simulées basées sur les tendances d'imagerie historique Landsat-8 et Sentinel-2.")

else:
    st.error(f"GeoJSON data file not found at {geojson_path}. Please check your repository structure.")
