function incrementValue(id) {
    const input = document.getElementById(id);
    const step = parseFloat(input.step) || 1;
    const max = parseFloat(input.max);
    let value = parseFloat(input.value) + step;
    
    if (input.max && value > max) {
        value = max;
    }
    
    input.value = id === 'cgpa' ? value.toFixed(1) : value;
}

function decrementValue(id) {
    const input = document.getElementById(id);
    const step = parseFloat(input.step) || 1;
    const min = parseFloat(input.min);
    let value = parseFloat(input.value) - step;
    
    if (input.min && value < min) {
        value = min;
    }
    
    input.value = id === 'cgpa' ? value.toFixed(1) : value;
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('prediction-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            
            if (data.error) {
                resultDiv.textContent = 'Error: ' + data.error;
                resultDiv.style.backgroundColor = '#ffebee';
            } else {
                resultDiv.innerHTML = `
                    <p><strong>${data.message}</strong></p>
                    <p>Confidence: ${data.probability}%</p>
                `;
                resultDiv.style.backgroundColor = data.prediction === 1 ? '#e8f5e9' : '#fff3e0';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').textContent = 'An error occurred during prediction.';
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').style.backgroundColor = '#ffebee';
        });
    });
});