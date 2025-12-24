document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const reviewText = document.getElementById('review-text');
    const reviewSubject = document.getElementById('review-subject');
    const reviewsContainer = document.getElementById('reviews-container');
    const ratingInput = document.getElementById('rating-value');
    const reviewerName = document.getElementById('reviewer-name');
    const stars = document.querySelectorAll('.stars i');

    // Star rating functionality
    stars.forEach(star => {
        // Handle hover effects
        star.addEventListener('mouseover', function() {
            const rating = this.getAttribute('data-rating');
            
            // Highlight stars on hover
            stars.forEach(s => {
                const sRating = s.getAttribute('data-rating');
                if (sRating <= rating) {
                    s.classList.remove('fa-regular');
                    s.classList.add('fa-solid');
                } else {
                    s.classList.remove('fa-solid');
                    s.classList.add('fa-regular');
                }
            });
        });

        // Handle mouse leaving the stars area
        document.querySelector('.stars').addEventListener('mouseleave', function() {
            const currentRating = ratingInput.value;
            
            // Reset to selected rating or all empty
            stars.forEach(s => {
                const sRating = s.getAttribute('data-rating');
                if (sRating <= currentRating) {
                    s.classList.remove('fa-regular');
                    s.classList.add('fa-solid');
                } else {
                    s.classList.remove('fa-solid');
                    s.classList.add('fa-regular');
                }
            });
        });

        // Handle star click
        star.addEventListener('click', function() {
            const rating = this.getAttribute('data-rating');
            ratingInput.value = rating;
            
            // Update visual state
            stars.forEach(s => {
                const sRating = s.getAttribute('data-rating');
                if (sRating <= rating) {
                    s.classList.remove('fa-regular');
                    s.classList.add('fa-solid');
                } else {
                    s.classList.remove('fa-solid');
                    s.classList.add('fa-regular');
                }
            });
        });
    });

    reviewForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const reviewContent = reviewText.value.trim();
        const subject = reviewSubject.value;
        const rating = ratingInput.value;
        const name = reviewerName.value.trim();

        if (!reviewContent) {
            alert('Please write a review before submitting.');
            return;
        }

        if (!subject) {
            alert('Please select a service to review.');
            return;
        }

        if (rating === '0') {
            alert('Please provide a star rating.');
            return;
        }

        if (!name) {
            alert('Please provide your name.');
            return;
        }

        // Get current date and time
        const now = new Date();
        const formattedDate = now.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        const formattedTime = now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        const dateTimeStr = `Posted on: ${formattedDate} at ${formattedTime}`;

        // Create and display the review
        const reviewElement = document.createElement('div');
        reviewElement.className = 'review-item';
        
        // Create review header with service name and star rating
        const reviewHeader = document.createElement('div');
        reviewHeader.className = 'review-header';
        
        const serviceTitle = document.createElement('h3');
        serviceTitle.textContent = subject;
        
        const ratingDisplay = document.createElement('div');
        ratingDisplay.className = 'rating-display';
        
        // Add stars to the rating display
        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('i');
            if (i <= rating) {
                star.className = 'fas fa-star';
            } else {
                star.className = 'far fa-star';
            }
            ratingDisplay.appendChild(star);
        }
        
        reviewHeader.appendChild(serviceTitle);
        reviewHeader.appendChild(ratingDisplay);
        
        // Create review meta section with reviewer name and date
        const reviewMeta = document.createElement('div');
        reviewMeta.className = 'review-meta';
        
        const nameSpan = document.createElement('span');
        nameSpan.className = 'reviewer-name';
        nameSpan.textContent = name;
        
        const dateSpan = document.createElement('span');
        dateSpan.className = 'review-date';
        dateSpan.textContent = dateTimeStr;
        
        reviewMeta.appendChild(nameSpan);
        reviewMeta.appendChild(dateSpan);
        
        // Create review content
        const reviewBody = document.createElement('p');
        reviewBody.textContent = reviewContent;
        
        // Append all elements to the review item
        reviewElement.appendChild(reviewHeader);
        reviewElement.appendChild(reviewMeta);
        reviewElement.appendChild(reviewBody);
        
        // Add the review to the container
        reviewsContainer.prepend(reviewElement);

        // Reset form
        reviewText.value = '';
        reviewSubject.selectedIndex = 0;
        ratingInput.value = '0';
        reviewerName.value = '';
        
        // Reset stars
        stars.forEach(s => {
            s.classList.remove('fa-solid');
            s.classList.add('fa-regular');
        });

        alert('Thank you for your review!');
    });
});