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
            // reset the select so user can pick another symptom
            symptomSelect.selectedIndex = 0;
        }
    });

    // Handle form submission via AJAX (improves UX and avoids full-page reloads)
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        // Get all selected symptoms
        let selected = Array.from(document.querySelectorAll(".tag")).map(tag => tag.textContent.trim());

        if (selected.length === 0) {
            alert("Please select at least one symptom");
            return;
        }

        // Disable submit while processing
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Analyzing...';

        // POST to JSON API
        fetch('/api/health_detector', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptoms: selected })
        })
        .then(resp => resp.json())
        .then(data => {
            // Replace selector UI with result container
            const resultHtml = `\n                <div class="result-container">\n                    <h3>Disease Prediction:</h3>\n                    <div class="prediction-result">${data.result}</div>\n                    <p>Note: This is only a preliminary assessment based on the symptoms provided. Please consult with a healthcare professional for a proper diagnosis.</p>\n                    <a href="/health_detector" class="new-prediction-btn">Start New Prediction</a>\n                </div>`;
            document.querySelector('.symptom-selector').outerHTML = resultHtml;
        })
        .catch(err => {
            console.error('Health detector request failed:', err);
            alert('Failed to analyze symptoms. Please try again.');
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        });
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
