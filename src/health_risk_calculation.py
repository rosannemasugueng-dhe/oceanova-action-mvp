def calculate_one_health_indices(satellite_fdi, stagnation_index, citizen_reports):
    """
    Computes the Dual One Health Risk Indices integrating orbital telemetry,
    field stagnation vectors, and human citizen science reports.
    """
    # 1. Global Risk Index (0-100): General population toxicity and water safety
    # Fuses satellite anomalies (40%), field stagnation (30%), and visual reporting density (30%)
    base_global = (satellite_fdi * 40) + (stagnation_index * 0.30) + (citizen_reports * 0.30)
    global_index = min(max(int(base_global), 0), 100)
    
    # 2. Maternal Endocrine Vulnerability Index (0-100): Isolates hormonal disruption hazards
    # Amplified by persistent water stagnation conditions which increase chemical concentration
    base_maternal = global_index * (1.15 if stagnation_index > 50 else 1.0)
    maternal_index = min(max(int(base_maternal), 0), 100)
    
    # 5-Tier Clinical Hazard Evaluation (Blue, Green, Yellow, Orange, Red)
    if maternal_index <= 15:
        hazard_level = "BLUE (0-15) - Ecological Sanctuary & Safe Baseline"
        marker_hex = "#1E88E5"
    elif maternal_index <= 35:
        hazard_level = "GREEN (16-35) - Low Risk & Routine Surveillance"
        marker_hex = "#43A047"
    elif maternal_index <= 55:
        hazard_level = "YELLOW (36-55) - Moderate Alert & Microplastic Detection"
        marker_hex = "#FDD835"
    elif maternal_index <= 75:
        hazard_level = "ORANGE (56-75) - High Risk & Priority Collection Zone"
        marker_hex = "#FB8C00"
    else:
        hazard_level = "RED (76-100) - Clinical Emergency & Endocrine Disruptor Hotspot"
        marker_hex = "#E53935"
        
    return {
        "global_risk_index": global_index,
        "maternal_endocrine_index": maternal_index,
        "hazard_level": hazard_level,
        "marker_hex": marker_hex
    }
