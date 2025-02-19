const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { predict_crop } = require('./backend/crop.py'); // Import your ML model function

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

app.post('/predict', (req, res) => {
    const { N, P, K, temperature, humidity, ph, rainfall } = req.body;
    const prediction = predict_crop(N, P, K, temperature, humidity, ph, rainfall);
    
    // Create a message based on the prediction
    const cropMessage = xyz(prediction); // Assume xyz returns a message
    res.json({ message: cropMessage });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
