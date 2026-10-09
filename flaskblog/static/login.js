document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const errorMessageDiv = document.getElementById('error-message');

    if (!loginForm) return;

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Stop default HTML page reloads

        // Reset error message state before submitting
        errorMessageDiv.classList.add('d-none');
        errorMessageDiv.innerText = '';

        // Extract values from Jinja form inputs by ID
        const emailInput = document.getElementById('email').value;
        const passwordInput = document.getElementById('password').value;
        const rememberInput = document.getElementById('remember') ? document.getElementById('remember').checked : false;

        const payload = {
            email: emailInput,
            password: passwordInput,
            remember: rememberInput
        };

        try {
            // Send JSON POST request to Flask backend
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            // Parse structured JSON response from Flask try/except routine
            const data = await response.json();

            if (response.ok && data.success) {
                // Successful auth: redirect to target page
                window.location.href = data.redirect_url;
            } else {
                // Backend caught an error/validation failure: render validation text
                displayError(data.message || 'An unexpected error occurred. Please try again.');
            }

        } catch (networkError) {
            // Handles server down or lost connection state
            displayError('Unable to connect to the server. Please check your network connection.');
        }
    });

    function displayError(message) {
        errorMessageDiv.innerText = message;
        errorMessageDiv.classList.remove('d-none');
    }
});