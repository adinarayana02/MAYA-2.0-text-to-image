const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

// Replace with your actual Monster API key
const MONSTER_API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjQzNDE2NzMyYWY4MDZkNzY4Y2RmZWNlNGEyY2NkNGNkIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDktMDFUMDU6NTQ6NTguMTc0MjQ2In0.RoF0q57NM2fQxIjb7HB1JnKVEgaF1SAMgB8HYPk_Mr8';

// Middleware to parse JSON bodies
app.use(express.json());

// Endpoint to generate an image
app.post('/generate-image', async (req, res) => {
    const prompt = req.body.prompt;

    if (!prompt) {
        return res.status(400).json({ error: 'Prompt is required' });
    }

    try {
        // Request to Monster API to generate the image
        const generateResponse = await axios.post('https://api.monster.ai/v1/generate', {
            model: 'sdxl-base',
            data: {
                prompt: prompt,
                negprompt: 'unreal, fake, meme, joke, disfigured, poor quality, bad, ugly',
                samples: 1,
                steps: 40,
                aspect_ratio: 'square',
                guidance_scale: 8.5
            }
        }, {
            headers: {
                'Authorization': `Bearer ${MONSTER_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        const processId = generateResponse.data.process_id;

        // Wait for the result (polling mechanism)
        let imageUrl = null;
        for (let i = 0; i < 10; i++) {
            await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds before polling again
            const resultResponse = await axios.get(`https://api.monster.ai/v1/results/${processId}`, {
                headers: {
                    'Authorization': `Bearer ${MONSTER_API_KEY}`
                }
            });

            if (resultResponse.data.status === 'completed') {
                imageUrl = resultResponse.data.output[0];
                break;
            }
        }

        if (imageUrl) {
            res.json({ imageUrl });
        } else {
            res.status(500).json({ error: 'Image generation failed or timed out' });
        }
    } catch (error) {
        console.error('Error generating image:', error);
        res.status(500).json({ error: 'An error occurred while generating the image' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
