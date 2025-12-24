document.addEventListener('DOMContentLoaded', () => {
    // References to form elements
    const appointmentForm = document.getElementById('appointment-form');
    const stateSelect = document.getElementById('state');
    const citySelect = document.getElementById('city');
    const dateInput = document.getElementById('appointment-date');
    
    // Set minimum date for appointment to today
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    dateInput.setAttribute('min', formattedDate);
    
    // City data for each state
    const cityData = {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Nellore", "Kurnool"],
        "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tawang"],
        "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon"],
        "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga"],
        "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba"],
        "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar"],
        "Haryana": ["Gurgaon", "Faridabad", "Rohtak", "Hisar", "Panipat", "Ambala"],
        "Himachal Pradesh": ["Shimla", "Dharamshala", "Mandi", "Solan", "Kullu"],
        "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh"],
        "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
        "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad"],
        "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Ukhrul"],
        "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongpoh"],
        "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Serchhip"],
        "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang"],
        "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur"],
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner"],
        "Sikkim": ["Gangtok", "Namchi", "Mangan", "Gyalshing"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
        "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailashahar"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Allahabad", "Ghaziabad"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur"],
        "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri"],
        "Delhi": ["New Delhi", "Delhi", "Noida", "Gurgaon", "Faridabad"]
    };

    // Handle state selection change
    stateSelect.addEventListener('change', () => {
        const selectedState = stateSelect.value;
        
        // Enable city dropdown
        citySelect.disabled = false;
        
        // Clear existing options
        citySelect.innerHTML = '<option value="" disabled selected>Select a city</option>';
        
        // Populate cities based on selected state
        if (selectedState && cityData[selectedState]) {
            cityData[selectedState].forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        } else {
            // If no state selected or no cities available, disable city dropdown
            citySelect.disabled = true;
            citySelect.innerHTML = '<option value="" disabled selected>Select a state first</option>';
        }
    });

    // Form submission handler
    appointmentForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const contact = document.getElementById('contact').value.trim();
        const reason = document.getElementById('reason').value.trim();
        const state = stateSelect.value;
        const city = citySelect.value;
        const appointmentDate = dateInput.value;
        const appointmentTime = document.getElementById('appointment-time').value;
        
        // Basic validation
        if (!name || !email || !contact || !reason || !state || !city || !appointmentDate || !appointmentTime) {
            alert('Please fill in all required fields.');
            return;
        }
        
        // Phone number validation (10 digits)
        if (!/^\d{10}$/.test(contact)) {
            alert('Please enter a valid 10-digit phone number.');
            return;
        }
        
        // Email validation
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            alert('Please enter a valid email address.');
            return;
        }
        
        // Format the appointment details for confirmation
        const appointmentDetails = {
            name,
            email,
            contact,
            reason,
            location: `${city}, ${state}`,
            appointmentDateTime: `${appointmentDate} at ${appointmentTime}`
        };
        
        // In a real application, this would submit the data to a server
        console.log('Appointment details:', appointmentDetails);
        
        // Show confirmation message
        alert(`Thank you, ${name}! Your appointment has been booked successfully for ${appointmentDate} at ${appointmentTime}.`);
        
        // Reset the form
        appointmentForm.reset();
        citySelect.disabled = true;
        citySelect.innerHTML = '<option value="" disabled selected>Select a state first</option>';
    });
});