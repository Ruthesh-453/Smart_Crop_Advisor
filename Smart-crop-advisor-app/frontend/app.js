document.getElementById('cropForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Get the input values
    const N = Number(document.getElementById('N').value);
    const P = Number(document.getElementById('P').value);
    const K = Number(document.getElementById('K').value);
    const temperature = Number(document.getElementById('temperature').value);
    const humidity = Number(document.getElementById('humidity').value);
    const ph = Number(document.getElementById('ph').value);
    const rainfall = Number(document.getElementById('rainfall').value);
    
    // Make a POST request to the backend
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ N, P, K, temperature, humidity, ph, rainfall }),
    });
    
    const data = await response.json();
    
    // Display the result
    document.getElementById('result').textContent = data.message;
});
