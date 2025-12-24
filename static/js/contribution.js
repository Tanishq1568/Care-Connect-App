document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const contributionForm = document.getElementById('contributionForm');
    const contributionType = document.getElementById('contributionType');
    const otherDescriptionGroup = document.getElementById('otherDescriptionGroup');
    const otherDescription = document.getElementById('otherDescription');
    const preferredDate = document.getElementById('preferredDate');
    
    
    // Get all contribution links
    const contributionLinks = document.querySelectorAll('a[data-contribution-type]');
    
    // Add click event listener to contribution links
    contributionLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default anchor behavior
            
            // Get the contribution type from the data attribute
            const type = this.getAttribute('data-contribution-type');
            
            // Set the select dropdown to the corresponding type
            if (type && ['blood', 'money', 'other'].includes(type)) {
                contributionType.value = type;
                
                // Trigger change event to show/hide other description field if needed
                const changeEvent = new Event('change');
                contributionType.dispatchEvent(changeEvent);
            }
            
            // Get the target element (the form)
            const targetElement = document.querySelector(this.getAttribute('href'));
            
            // Smooth scroll to the form
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
                
                // Focus on the form after scrolling
                setTimeout(() => {
                    contributionType.focus();
                }, 800);
            }
        });
    });
    
    // Show/hide other description based on contribution type
    contributionType.addEventListener('change', function() {
        if (this.value === 'other') {
            otherDescriptionGroup.style.display = 'block';
            otherDescription.setAttribute('required', true);
        } else {
            otherDescriptionGroup.style.display = 'none';
            otherDescription.removeAttribute('required');
        }
    });
    
    // Form submission handler
    contributionForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Get form values
        const type = contributionType.value;
        const name = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        let description = '';
        
        if (type === 'other') {
            description = otherDescription.value;
        } else if (type === 'blood') {
            description = 'Blood Donation';
        } else if (type === 'money') {
            description = 'Financial Contribution';
        }
        
        // Create contribution data object
        const contributionData = {
            type,
            description,
            name,
            email,
            phone,
        };
        
        // Log data (in real application, this would be sent to a server)
        
        // Show success message
        alert(`Thank you, ${name}! Your ${description} contribution has been registered. We will contact you soon.`);
        
        // Reset form
        contributionForm.reset();
        otherDescriptionGroup.style.display = 'none';
    });
});