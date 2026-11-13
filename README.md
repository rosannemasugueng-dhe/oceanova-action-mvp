# OceaNova Action — One Health Predictive Dashboard

[![Python Version](https://shields.io)](https://python.org)
[![Framework](https://shields.io)](https://streamlit.io)
[![Status](https://shields.io)]([https://github.com](https://github.com/rosannemasugueng-dhe/oceanova-action-mvp.git
))

OceaNova Action is an agile DeepTech platform engineered under the **"One Health"** lens. It bridges the structural gap between real-time environmental space observations and proactive public health interventions. By detecting riverine, lacustrine, and marine plastic accumulation trajectories across Africa via remote sensing, the platform dynamically computes a predictive Microplastic Health Risk Index to safeguard coastal and riparian communities against endocrine-disrupting toxicity.
---

## Key Innovation Frameworks

* **Multi-Source Data Fusion:** Interconnecting macro-environmental orbital observations with localized, un-mapped citizen science inputs from artisanal fishers.
* **Predictive Toxicological Modeling:** Translating plastic stagnation density and geographic drainage matrices into real-time bioaccumulation hazard warnings for regional health institutions.
---

## Software Architecture & Core Modules

The repository follows a clean, modular structure separating the data ingestion, core calculation matrix, and frontend visualization layer:

```text
oceanova-action-mvp/
├── data/
│   └── points_impact_africa.geojson   # High-resolution spatial risk coordinates
├── src/
│   ├── __init__.py
│   ├── health_risk_calculation.py    # Clinical risk fusion matrix
│   └── ingestion_satellite.py         # Space observation mock engine
├── .gitignore
├── LICENSE                            # Legal open-source distribution framework
├── README.md
├── logo.jpeg                          # Official application badge
├── requirements.txt                   # Project package dependencies
└── app.py                             # Core execution dashboard
```

### 1. Frontend Core (`app.py`)
* Serves as the platform's orchestration hub built entirely via Streamlit.
* Implements multi-layered geospatial mapping using Folium and GeoJSON specs (`data/points_impact_africa.geojson`).
* Integrates a live user-facing Citizen Science Input Pipeline inside the sidebar, enabling immediate, ground-truthed field reporting that re-computes the map state instantly.
* Implements dynamic, multi-variable filtering (by Country and Ecosystem type) with reactive metric dashboards.

### 2. Satellite Earth Observation Engine (`src/ingestion_satellite.py`)
* Simulates and compiles structured OData queries targeting the ESA Copernicus Data Space Ecosystem (CDSE) and NASA GIBS catalog.
* Formulates automated bounding geospatial queries utilizing the `OData.CSC.Intersects(footprint=...)` standard with a strict atmospheric boundary constraint (`cloudCover lt 15.0`).
* Emulates near-infrared and shortwave-infrared (SWIR) anomalies to calculate the Floating Debris Index (FDI) for specific African waterways.
* Engineered with a fail-safe exception pipeline ensuring zero runtime dashboard crashes during offline or low-bandwidth operations.

### 3. Clinical Risk Fusion Matrix (`src/health_risk_calculation.py`)
* Acts as the decision-intelligence layer mapping ecological data onto clinical vulnerability parameters.
* Integrates the orbital Plastic Signature Confidence with local geographic hydrology factors (such as the Water Stagnation Index or artificial blockages).
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
git clone [https://github.com](https://github.com/rosannemasugueng-dhe/oceanova-action-mvp.git)
cd oceanova-action-mvp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Spin up the One Health Predictive Interface
python -m streamlit run app.py --server.clearCache=true
```
---

## Executive Credits
Developed by **Rosanne Masugue Ngangoumoun** — Software Engineering Student at African Leadership University (ALU) & Millennium Fellow class of 2026.



# OceaNova Action Inc. — One Health Predictive & Circular DeepTech Infrastructure

![Python Version](https://shields.io)
![Framework](https://shields.io)
![Database](https://shields.io)
![License](https://shields.io)
![UN SDGs](https://shields.io)

**OceaNova Action Inc.** is an enterprise-grade DeepTech and **One Health** infrastructure engineered to bridge the gap between real-time orbital Earth observation, proactive maternal healthcare, and inclusive circular industrialization. 

By fusing **NASA (VIIRS)** and **ESA Copernicus (Sentinel-2 MSI L2A)** satellite telemetry with ground-level citizen science data, the platform detects riverine and marine plastic accumulation hotspots across Africa at the source. It computes a context-aware **Dual-Risk Index** and converts environmental threats into dignified, circular green livelihoods through a self-sustaining **Textile-to-Cash** and **B2G SaaS** model.

---

## Systemic Impact: Solving 9 UN Sustainable Development Goals (SDGs)

Originally conceived around marine conservation (SDG 14), **OceaNova Action Inc.** has evolved into an integrated systemic engine directly addressing **9 United Nations Sustainable Development Goals** simultaneously:

| UN SDG | Strategic Pillar | Concrete Mechanism & Measurable Impact |
| :--- | :--- | :--- |
| **SDG 1** | **No Poverty** | Replaces short-term charity with direct, predictable daily income (\$0.25/kg via instant Mobile Money) for low-income households along polluted waterways. |
| **SDG 3** | **Good Health & Well-being** | Deploys a **Maternal Endocrine Vulnerability Index** protecting pregnant women and young girls from hormone-disrupting microplastics, safeguarding future generations. |
| **SDG 6** | **Clean Water & Sanitation** | Monitors drinking water sources in real time via satellite and intercepts plastic contaminants before they degrade municipal and rural water supplies. |
| **SDG 8** | **Decent Work & Economic Growth** | Creates dignified, barrier-free green jobs explicitly accessible to **both literate and non-literate individuals**, scaling from Africa first to the global stage. |
| **SDG 9** | **Industry, Innovation & Infrastructure** | Builds sovereign African geospatial AI infrastructure alongside local textile-upcycling micro-factories producing certified recycled polyester thread. |
| **SDG 12** | **Responsible Consumption & Production** | Closes the plastic loop by transforming riverine waste into traceable, certified recycled polyester yarn equipped with unique digital origin passports. |
| **SDG 13** | **Climate Action** | Reduces carbon emissions, prevents open plastic burning, mitigates urban/riverine thermal stress, and empowers local communities as active climate stewards. |
| **SDG 14** | **Life Below Water** | Intercepts ocean-bound plastic directly inside river basins (Wouri, Nyabarongo, Niger, Nairobi, Sanaga), protecting aquatic biodiversity and artisanal fisheries. |
| **SDG 17** | **Partnerships for the Goals** | Unites open space agencies (NASA/ESA), Ministries of Health, global apparel supply chains, academic institutions, and local communities on one platform. |

---

## Key Innovation Frameworks

* **Multi-Source Orbital & Ground Data Fusion:** Interconnects macro-environmental satellite observations with localized, ground-truthed citizen science telemetry from artisanal fishers and community health workers.
* **5-Tier Clinical & Toxicological Modeling:** Translates water stagnation matrices and plastic spectral anomalies into a high-precision **5-level clinical hazard spectrum** (*Blue 0–15, Green 16–35, Yellow 36–55, Orange 56–75, Red 76–100*) to guide urgent public health interventions.
* **Self-Sustaining Dual Business Engine:** 
  * *B2B Circular Track ("Textile-to-Cash"):* Leverages global fashion supply chain demand to fund community plastic collection and local upcycling into certified recycled polyester thread.
  * *B2G One Health SaaS:* Provides regional Ministries of Health and municipal councils with tiered epidemiological risk mapping licenses.

---

## Software Architecture & Core Modules

The repository follows a modular, production-ready architecture separating data ingestion, clinical risk computation, persistent storage, and interactive bilingual visualization:

```text
oceanova-action-mvp/
├── data/
│   └── points_impact_africa.geojson   # Spatial risk coordinates & baseline telemetry
├── src/
│   ├── __init__.py
│   ├── health_risk_calculation.py     # Dual-Risk & 5-tier clinical fusion matrix
│   └── ingestion_satellite.py         # ESA Copernicus CDSE & NASA GIBS OData engine
├── .gitignore                         # Protects private databases, keys & local caches
├── LICENSE                            # Open-source MIT License framework
├── README.md                          # Executive & technical documentation
├── app.py                             # Core Streamlit bilingual orchestration dashboard
├── database.py                        # SQLAlchemy persistent database layer (PostGIS-ready)
├── logo.jpeg                          # Official OceaNova Action application emblem
└── requirements.txt                   # Project dependencies
```

### 1. Frontend Core & Interactive Registry (`app.py`)
* Serves as the platform's bilingual (**English / Français**) orchestration hub built with Streamlit.
* Renders interactive geospatial risk mapping via **Folium** using a **5-tier color-coded clinical scale** (`#1E88E5` Blue, `#43A047` Green, `#FDD835` Yellow, `#FB8C00` Orange, `#E53935` Red).
* Features a live **Citizen Science Input Pipeline** with automated geocoding (`Geopy / Nominatim`), dynamic country/ecosystem filtering, a real-time **Textile-to-Cash econometric simulator**, and a **bilingual CRUD waterway registry** with row-level management.

### 2. Persistent Spatial Database Layer (`database.py`)
* Powered by **SQLAlchemy** (`SQLite` locally, seamlessly migratable to **PostgreSQL / PostGIS** in cloud production).
* Ensures zero data loss across sessions and browser refreshes while maintaining strict privacy isolation via `.gitignore`.

### 3. Satellite Earth Observation Engine (`src/ingestion_satellite.py`)
* Compiles structured OData queries targeting the **ESA Copernicus Data Space Ecosystem (CDSE)** (`catalogue.dataspace.copernicus.eu`) and NASA GIBS catalog.
* Applies strict geospatial bounding filters (`OData.CSC.Intersects`) and atmospheric constraints (`cloudCover lt 15.0`) to evaluate Floating Debris Index (FDI) spectral anomalies with an offline fail-safe pipeline.

### 4. Clinical Risk Fusion Matrix (`src/health_risk_calculation.py`)
* Computes both the **Global Risk Index (0–100)** and the **Maternal Endocrine Vulnerability Index (0–100)** by fusing satellite plastic confidence with hydrological stagnation vectors and citizen reports.

---

## Technical Stack

* **Language:** Python 3.10+
* **Frontend & Visualization:** Streamlit, Folium, Branca, Streamlit-Folium
* **Database & ORM:** SQLAlchemy (SQLite / PostGIS-ready)
* **Geospatial & Analytics:** Pandas, Geopy (Nominatim), GeoJSON (EPSG:4326)
* **Satellite Data Standards:** ESA Copernicus Sentinel-2 MSI L2A (OData) & NASA VIIRS

---

## Local Setup & Execution Roadmap

To run the full One Health Predictive Dashboard locally, execute the following commands:

```bash
# 1. Clone the repository
git clone https://github.com/rosannemasugueng-dhe/oceanova-action-mvp.git
cd oceanova-action-mvp

# 2. Install required dependencies
pip install -r requirements.txt

# 3. Launch the OceaNova Action dashboard
python -m streamlit run app.py --server.clearCache=true
```

---

## Executive Credits & Recognition

Architected and developed by **Rosanne Masugue Ngangoumoun** — Founder & CEO of **OceaNova Action Inc.**, Software Engineering Student at the **African Leadership University (ALU Kigali)**, **2026 Millennium Fellow**, and Official Delegate selected by the **African Union (Africa CDC)** for **CPHIA 2026**.

*Licensed under the MIT License — Open-source transparency for global planetary and maternal health.*
