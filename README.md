# OceaNova Action — One Health Predictive Dashboard

OceaNova Action is an agile DeepTech platform engineered under the **"One Health" lens**. It bridges the structural gap between real-time environmental space observations and proactive public health interventions. By detecting riverine, lacustrine, and marine plastic accumulation trajectories across Africa via remote sensing, the platform dynamically computes a predictive **Microplastic Health Risk Index** to safeguard coastal and riparian communities against endocrine-disrupting toxicity.

## Key Innovation Frameworks

* **Multi-Source Data Fusion:** Interconnecting macro-environmental orbital observations with localized, un-mapped citizen science inputs from artisanal fishers.
* **Predictive Toxicological Modeling:** Translating plastic stagnation density and geographic drainage matrices into real-time bioaccumulation hazard warnings for regional health institutions.
---

## Software Architecture & Core Modules

The pipeline is split into modular components designed to support clean integration from simulated scenarios to live telemetry:
### 1. Frontend Core (`app.py`)
* Serves as the platform's orchestration hub built entirely via **Streamlit**.
* Implements multi-layered geospatial mapping using **Folium** and **GeoJSON** specs (`data/points_impact_africa.geojson`).
* Integrates a live user-facing **Citizen Science Input Pipeline** inside the sidebar, enabling immediate, ground-truthed field reporting that re-computes the map state instantly.
* Implements dynamic, multi-variable filtering (by Country and Ecosystem type) with reactive metric dashboards.

### 2. Satellite Earth Observation Engine (`src/ingestion_satellite.py`)
* Simulates and compiles structured `OData` queries targeting the **ESA Copernicus Data Space Ecosystem (CDSE)** and **NASA GIBS catalog**.
* Formulates automated bounding geospatial queries utilizing the `OData.CSC.Intersects(footprint=...)` standard with a strict atmospheric boundary constraint (`cloudCover lt 15.0`).
* Emulates near-infrared and shortwave-infrared (SWIR) anomalies to calculate the **Floating Debris Index (FDI)** for specific African waterways.
* Engineered with a fail-safe exception pipeline ensuring zero runtime dashboard crashes during offline or low-bandwidth operations.

### 3. Clinical Risk Fusion Matrix (`src/health_risk_calculation.py`)
* Acts as the decision-intelligence layer mapping ecological data onto clinical vulnerability parameters.
* Integrates the orbital **Plastic Signature Confidence** with local geographic hydrology factors (such as the *Water Stagnation Index* or artificial blockages).
* Classifies systemic threats into a tripartite hazard spectrum, issuing proactive alerts regarding potential endocrine disruptors and biomagnification risks affecting maternal health ecosystems.
---

## Technical Stack

* **Language:** Python 3.10+
* **Dashboard Interface:** Streamlit Framework
* **Geospatial Processing:** Folium, Branca, and GeoJSON (EPSG:4326)
* **Data Structures:** Pandas Analytics Engine
* **Satellite Sources:** NASA GIBS (VIIRS) & ESA Copernicus (Sentinel-2 MSI L2A)
---

## Local Setup & Execution Roadmap

To run the full dashboard ecosystem locally, execute the following sequences within your Python environment:
```bash
# 1. Clone the environment repository
git clone https://github.com
cd oceanova-action-mvp

# 2. Install dependencies (including pandas for data arrays)
pip install -r requirements.txt

# 3. Spin up the One Health Predictive Interface
python -m streamlit run app.py --server.clearCache=true
```

Developed by **Rosanne Masugue Ngangoumoun** — *Software Engineering Student at African Leadership University (ALU) & Millennium Fellow class of 2026.*
