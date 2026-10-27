import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os

# Configuration de la page Streamlit
st.set_page_config(page_title="OceaNova Action MVP", page_icon="🌍", layout="wide")

st.title("🌍 OceaNova Action — One Health Predictive Dashboard")
st.markdown("### Early-Warning System for Riverine Microplastic Risks & Maternal Health Protection")

# Sidebar d'informations
st.sidebar.image("https://icons8.com", width=80)
st.sidebar.header("System Controls")
st.sidebar.markdown("**Founder & CEO:** Rosanne Masugue Ngangoumoun")
st.sidebar.markdown("**Status:** Active Development (Simulated Pipeline)")

# Vérification et chargement du fichier GeoJSON
geojson_path = "data/points_impact_afrique.geojson"

if os.path.exists(geojson_path):
    with open(geojson_path, "r") as f:
        data = json.load(f)
    
    # Métriques globales
    col1, col2, col3 = st.columns(3)
    col1.metric("Monitored Hotspots", len(data["features"]), "Inland Waterways")
    col2.metric("Highest Risk Index", "95/100", "Wouri River, Cameroon", delta_color="inverse")
    col3.metric("Active Field Responders", "150+ Artisanal Fishers", "Rwanda & Cameroon")

    st.markdown("---")
    st.subheader("📍 Live Microplastic Risk Mapping (One Health Trajectory)")

    # Initialisation de la carte Folium centrée sur l'Afrique Centrale
    m = folium.Map(location=[1.0, 20.0], zoom_start=4, tiles="CartoDB positron")

    # Ajout des marqueurs à partir du GeoJSON
    for feature in data["features"]:
        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]
        
        # Inversion des coordonnées pour Folium (Folium utilise [Latitude, Longitude])
        lat, lon = coords[1], coords[0]
        
        # Couleur du marqueur selon le risque
        color = "red" if props["risk_index"] > 80 else "orange"
        
        # Contenu de la popup
        popup_text = f"""
        <div style='font-family: Arial, sans-serif; width: 200px;'>
            <h4>{props['location_name']}</h4>
            <b>Risk Index:</b> {props['risk_index']}/100<br>
            <b>Maternal Hazard:</b> <span style='color:red;'>{props['maternal_health_hazard']}</span><br>
            <b>Community Status:</b> {props['community_status']}
        </div>
        """
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

    # Affichage de la carte dans Streamlit
    st_folium(m, width=1100, height=500)

else:
    st.error(f"GeoJSON data file not found at {geojson_path}. Please check your repository structure.")
