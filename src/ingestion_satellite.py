import random

def fetch_satellite_metadata(coordinates):
    """
    Simulates fetching open-source ESA Sentinel / NASA satellite metadata 
    for plastic spectral signature detection.
    """
    lat, lon = coordinates
    print(f"[INFO] Connecting to Copernicus Data Space Ecosystem API for coordinates: {lat}, {lon}")
    
    # Simulated spectral anomaly detection (plastic reflection coefficient)
    spectral_anomaly = round(random.uniform(0.1, 0.9), 2)
    
    return {
        "sensor_id": "SENTINEL-2_MSI",
        "cloud_cover_percentage": round(random.uniform(0.0, 15.0), 2),
        "plastic_signature_confidence": spectral_anomaly
    }
