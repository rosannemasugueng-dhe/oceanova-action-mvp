def calculate_one_health_indices(satellite_fdi, stagnation_index, citizen_reports):
    """
    Computes the Dual One Health Risk Indices integrating orbital telemetry,
    field stagnation vectors, and human citizen science reports.
    """
    # 1. Global Risk Index (0-100): General population toxicity and water safety
    # Fuses satellite anomalies (40%), field stagnation (30%), and visual reporting density (30%)
    base_global = (satellite_fdi * 40) + ((stagnation_index / 100) * 30) + ((citizen_reports / 100) * 30)
    global_index = min(max(int(base_global * 100), 0), 100)
    
    # 2. Maternal Endocrine Vulnerability Index (0-100): Isolates hormonal disruption hazards
    # Amplified by persistent water stagnation conditions which increase chemical concentration
    base_maternal = global_index * (1.15 if stagnation_index > 50 else 1.0)
    maternal_index = min(max(int(base_maternal), 0), 100)
    
    # Tripartite Clinical Hazard Evaluation
    if maternal_index > 75:
        hazard_level = "CRITICAL - Endocrine Disruptor & Toxin Bioaccumulation Alert"
    elif maternal_index > 45:
        hazard_level = "MODERATE - Increased Clinical & Field Monitoring Required"
    else:
        hazard_level = "LOW - Stable Baseline Environmental Threshold"
        
    return {
        "global_risk_index": global_index,
        "maternal_endocrine_index": maternal_index,
        "hazard_level": hazard_level
    }
