document.addEventListener("DOMContentLoaded", function (){
    const symptoms = [
        "Abdominal Pain", "Appetite Changes", "Bad Breath", "Bleeding Gums", "Bloating", "Blood in Urine", "Blurred Vision",
        "Body Ache", "Bone Fractures", "Bullseye Rash", "Chest Pain", "Chest Tightness", "Chills", "Cold Sweat",
        "Confusion", "Constipation", "Cracked Skin", "Cough", "Dark Urine", "Diarrhea", "Difficulty Breathing",
        "Difficulty Speaking", "Difficulty Swallowing", "Dizziness", "Excessive Salivation", "Excessive Thirst",
        "Excessive Worry", "Facial Pain", "Fatigue", "Fever", "Frequent Urination", "Gas", "Hair Loss", "Hallucinations",
        "Headache", "Heartburn", "High Fever", "Itchiness", "Itchy Circular Rash", "Itchy Rash", "Jaundice", "Jaw Lock",
        "Joint Pain", "Lightheadedness", "Loss of Appetite", "Loss of Balance", "Loss of Consciousness",
        "Loss of Coordination", "Loss of Height", "Loss of Interest", "Loss of Taste", "Memory Loss", "Mood Changes",
        "Mucus Production", "Muscle Jerking", "Muscle Pain", "Muscle Stiffness", "Nasal Congestion", "Nausea",
        "Night Sweats", "Numbness", "Painful Urination", "Pale Skin", "Paralysis", "Pelvic Pain", "Rapid Heartbeat",
        "Rash", "Red Patches", "Red Spots", "Regurgitation", "Restlessness", "Runny Nose", "Sadness", "Scaly Skin",
        "Seizures", "Sensitivity to Light", "Severe Back Pain", "Severe Headache", "Shortness of Breath", "Skin Rash",
        "Sleep Disturbances", "Slow Movement", "Sneezing", "Sore Throat", "Staring Spells", "Stiff Muscles",
        "Stomach Cramps", "Stomach Pain", "Stooped Posture", "Sudden Numbness", "Sweating", "Swollen Glands",
        "Swollen Neck", "Swollen Tonsils", "Tremors", "Trouble Speaking", "Unexplained Weight Loss", "Vision Problems",
        "Vomiting", "Weakness", "Weight Loss", "Wheezing", "Yellow Eyes", "Yellow Skin"
      ];
      
    const symptomSelect = document.getElementById("symptom-select");
    const selectedSymptomsDiv = document.getElementById("selectedSymptoms");
    const hiddenInput = document.getElementById("hiddenSymptoms");
    const form = document.querySelector("form");

    symptoms.forEach(symptom =>{
        let option = document.createElement("option");
        option.value = symptom;
        option.textContent = symptom;
        symptomSelect.appendChild(option);
    });

    symptomSelect.addEventListener("change", function (){
        let selectedSymptom = symptomSelect.value;
        if(selectedSymptom){
            addSymptom(selectedSymptom);
        }
    });

    // Handle form submission
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        
        // Get all selected symptoms
        let selected = Array.from(document.querySelectorAll(".tag")).map(tag => tag.textContent);
        
        // Clear existing hidden inputs
        const existingInputs = document.querySelectorAll('input[name="symptoms"]');
        existingInputs.forEach(input => input.remove());
        
        // Create a hidden input for each symptom
        selected.forEach(symptom => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'symptoms';
            input.value = symptom;
            form.appendChild(input);
        });
        
        // Submit the form if we have symptoms
        if (selected.length > 0) {
            form.submit();
        } else {
            alert("Please select at least one symptom");
        }
    });

    function addSymptom(symptom){
        let existingTags = Array.from(document.querySelectorAll(".tag")).map(tag => tag.textContent);
        if(!existingTags.includes(symptom)){
            let tag = document.createElement("div");
            tag.classList.add("tag");
            tag.textContent = symptom;
            tag.onclick = function (){
                tag.remove();
            };
            selectedSymptomsDiv.appendChild(tag);
        }
    }
});
