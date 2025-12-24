document.addEventListener("DOMContentLoaded", function (){
    fetch('/get_emergency_list')
        .then(response => response.json())
        .then(data =>{
            const emergencySelect = document.getElementById("emergency");
            data.emergencies.forEach(emergency => {
                let option = document.createElement("option");
                option.value = emergency;
                option.textContent = emergency;
                emergencySelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching emergency list:', error));
});

function getEmergencySteps(){
    const selectedEmergency = document.getElementById("emergency").value;
    
    fetch('/get_emergency_steps',{
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emergency: selectedEmergency })
    })
    .then(response => response.json())
    .then(data => {
        const stepsContainer = document.getElementById("steps-container");
        stepsContainer.innerHTML = `<h2>First Aid Steps:</h2><ul>` +
            data.steps.map(step => `<li>${step}</li>`).join('') + `</ul>`;
    })
    .catch(error => console.error('Error fetching steps:', error));
}