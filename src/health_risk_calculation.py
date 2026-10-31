def evaluate_one_health_risk(satellite_confidence, water_stagnation_factor=1.0):
    """
    Computes the Microplastic Health Risk Index integrating environmental matrices 
    with clinical bioaccumulation risk parameters for maternal health.
    """
    # Algorithmic fusion of satellite observations and ground-based parameters
    base_risk = (satellite_confidence * 60) + (water_stagnation_factor * 40)
    final_index = min(int(base_risk), 100)
    
    if final_index > 80:
        hazard_level = "Critical - Endocrine Disruptor & Toxin Bioaccumulation Alert"
    elif final_index > 50:
        hazard_level = "Moderate - Increased Monitoring Required"
    else:
        hazard_level = "Low - Stable Baseline"
        
    return {
        "calculated_index": final_index,
        "maternal_health_hazard": hazard_level
    }
