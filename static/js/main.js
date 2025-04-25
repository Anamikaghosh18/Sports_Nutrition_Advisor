document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analyzeForm');
    const sportSelect = document.getElementById('sport');
    const otherSportGroup = document.getElementById('otherSportGroup');
    const otherSportInput = document.getElementById('otherSport');
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    const previewContainer = document.querySelector('.preview-container');
    const loader = document.getElementById('loader');
    const results = document.getElementById('results');
    const analysisContent = document.getElementById('analysisContent');
    
    // Show/hide other sport input based on selection
    sportSelect.addEventListener('change', function() {
        if (this.value === 'Other') {
            otherSportGroup.classList.remove('hidden');
            otherSportInput.required = true;
        } else {
            otherSportGroup.classList.add('hidden');
            otherSportInput.required = false;
        }
    });
    
    // Show image preview
    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewContainer.classList.remove('hidden');
            }
            reader.readAsDataURL(file);
        }
    });
    
    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        if (!validateForm()) {
            return;
        }
        
        // Show loader
        loader.classList.remove('hidden');
        results.classList.add('hidden');
        
        // Create form data
        const formData = new FormData();
        const sportValue = sportSelect.value === 'Other' ? otherSportInput.value : sportSelect.value;
        
        formData.append('sport', sportValue);
        formData.append('image', imageInput.files[0]);
        
        // Send request to server
        fetch('/analyze', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Hide loader
            loader.classList.add('hidden');
            
            if (data.success) {
                // Show results
                results.classList.remove('hidden');
                
                // Format the analysis with better styling
                const formattedText = formatAnalysisText(data.analysis);
                analysisContent.innerHTML = formattedText;
                
                // Scroll to results
                results.scrollIntoView({ behavior: 'smooth' });
            } else {
                showError('Analysis Error', data.error);
            }
        })
        .catch(error => {
            loader.classList.add('hidden');
            showError('Request Error', error.message);
        });
    });
    
    // Validate form before submission
    function validateForm() {
        if (sportSelect.value === '') {
            showError('Validation Error', 'Please select a sport');
            return false;
        }
        
        if (sportSelect.value === 'Other' && otherSportInput.value.trim() === '') {
            showError('Validation Error', 'Please specify the sport');
            return false;
        }
        
        if (!imageInput.files || imageInput.files.length === 0) {
            showError('Validation Error', 'Please select an image to analyze');
            return false;
        }
        
        return true;
    }
    
    // Format analysis text with better styling
    function formatAnalysisText(text) {
        // Add section styling
        text = text.replace(/^(#+ .+)$/gm, '<h3 class="section-title">$1</h3>');
        
        // Convert line breaks to paragraph tags
        text = text.replace(/\n\n/g, '</p><p>');
        
        // Style lists
        text = text.replace(/^(\d+\.\s+)(.+)$/gm, '<div class="list-item"><span class="list-number">$1</span>$2</div>');
        
        // Wrap in paragraphs
        text = '<p>' + text + '</p>';
        
        return text;
    }
    
    // Show error message
    function showError(title, message) {
        alert(`${title}: ${message}`);
    }

    document.getElementById('sendChatbotMessage').addEventListener('click', async () => {
        const inputField = document.getElementById('chatbotInput');
        const userMessage = inputField.value.trim();
        if (!userMessage) return;

        // Display user message
        const messagesContainer = document.getElementById('chatbot-messages');
        const userMessageElement = document.createElement('div');
        userMessageElement.className = 'message user';
        userMessageElement.textContent = userMessage;
        messagesContainer.appendChild(userMessageElement);

        // Clear input field
        inputField.value = '';

        // Send message to backend
        try {
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage })
            });
            const data = await response.json();

            // Display chatbot response
            const botMessageElement = document.createElement('div');
            botMessageElement.className = 'message bot';
            botMessageElement.textContent = data.response || 'Sorry, I could not process your request.';
            messagesContainer.appendChild(botMessageElement);

            // Scroll to the bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        } catch (error) {
            console.error('Error:', error);
        }
    });
});