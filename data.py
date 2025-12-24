disease_rules = {
    # Common Diseases
    "Flu": ["fever", "cough", "body ache", "fatigue", "headache"],
    "Cold": ["sneezing", "runny nose", "sore throat", "cough", "mild fever"],
    "Malaria": ["fever", "chills", "headache", "sweating", "nausea"],
    "Typhoid": ["fever", "stomach pain", "weakness", "loss of appetite", "constipation"],
    "Dengue": ["high fever", "severe headache", "joint pain", "rash", "bleeding gums"],
    "COVID-19": ["fever", "cough", "shortness of breath", "loss of taste", "fatigue"],
    "Pneumonia": ["fever", "cough", "chest pain", "difficulty breathing", "chills"],
    "Asthma": ["shortness of breath", "wheezing", "chest tightness", "cough"],
    "Bronchitis": ["cough", "mucus production", "fatigue", "shortness of breath", "chills"],
    "Sinusitis": ["facial pain", "nasal congestion", "runny nose", "headache", "cough"],
    "Tuberculosis": ["cough", "fever", "weight loss", "night sweats", "chest pain"],
    "Tonsillitis": ["sore throat", "difficulty swallowing", "fever", "bad breath", "swollen tonsils"],
    
    # Digestive System Diseases
    "Appendicitis": ["abdominal pain", "nausea", "vomiting", "loss of appetite", "fever"],
    "Food Poisoning": ["nausea", "vomiting", "diarrhea", "stomach cramps", "fever"],
    "Acid Reflux": ["heartburn", "chest pain", "difficulty swallowing", "regurgitation"],
    "Gastritis": ["stomach pain", "bloating", "nausea", "vomiting", "loss of appetite"],
    "Hepatitis": ["jaundice", "fatigue", "nausea", "abdominal pain", "dark urine"],
    "Jaundice": ["yellow skin", "yellow eyes", "fatigue", "abdominal pain", "dark urine"],
    "Irritable Bowel Syndrome (IBS)": ["abdominal pain", "bloating", "diarrhea", "constipation", "gas"],

    # Neurological & Mental Health Disorders
    "Migraine": ["headache", "nausea", "sensitivity to light", "blurred vision", "dizziness"],
    "Epilepsy": ["seizures", "confusion", "staring spells", "loss of consciousness", "muscle jerking"],
    "Depression": ["sadness", "loss of interest", "fatigue", "sleep disturbances", "appetite changes"],
    "Anxiety": ["excessive worry", "restlessness", "difficulty sleeping", "rapid heartbeat", "sweating"],
    "Parkinson’s Disease": ["tremors", "slow movement", "stiff muscles", "loss of balance"],
    "Alzheimer’s Disease": ["memory loss", "confusion", "difficulty speaking", "mood changes"],
    
    # Chronic Conditions
    "Diabetes": ["frequent urination", "excessive thirst", "unexplained weight loss", "fatigue"],
    "Hypertension": ["headache", "chest pain", "blurred vision", "shortness of breath"],
    "Anemia": ["fatigue", "weakness", "pale skin", "shortness of breath", "dizziness"],
    "Osteoporosis": ["back pain", "bone fractures", "stooped posture", "loss of height"],
    "Arthritis": ["joint pain", "swelling", "stiffness", "reduced mobility", "fatigue"],
    
    # Skin & Infectious Diseases
    "Chickenpox": ["itchy rash", "fever", "fatigue", "loss of appetite", "red spots"],
    "Measles": ["rash", "fever", "cough", "runny nose", "red eyes"],
    "Mumps": ["swollen glands", "fever", "headache", "muscle pain", "loss of appetite"],
    "Ringworm": ["itchy circular rash", "scaly skin", "red patches", "hair loss"],
    "Eczema": ["dry skin", "itchiness", "redness", "cracked skin", "swelling"],

    # Urinary & Kidney Diseases
    "Kidney Stones": ["severe back pain", "blood in urine", "nausea", "vomiting", "painful urination"],
    "Urinary Tract Infection (UTI)": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain"],
    
    # Heart & Circulatory System Diseases
    "Heart Attack": ["chest pain", "shortness of breath", "nausea", "cold sweat", "lightheadedness"],
    "Stroke": ["sudden numbness", "trouble speaking", "confusion", "loss of coordination"],

    # Rare but Important Diseases
    "Lupus": ["joint pain", "skin rash", "fatigue", "fever", "chest pain"],
    "Multiple Sclerosis": ["vision problems", "weakness", "loss of balance", "numbness", "fatigue"],
    "Lyme Disease": ["bullseye rash", "fatigue", "fever", "joint pain", "headache"],
    "Diphtheria": ["sore throat", "difficulty breathing", "swollen neck", "fever"],
    "Rabies": ["hallucinations", "fever", "excessive salivation", "paralysis"],
    "Tetanus": ["muscle stiffness", "jaw lock", "fever", "difficulty swallowing"],
}
