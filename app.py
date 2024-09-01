import streamlit as st
import os
import requests
from monsterapi import client
from io import BytesIO
import streamlit.components.v1 as components
from flask import Flask, request, jsonify

# Set up Flask server within Streamlit
app = Flask(__name__)

# Function to generate images using Monster API
def imagen(prompt):
    os.environ['MONSTER_API_KEY'] = os.getenv('MONSTERAI_API_KEY')
    monster_client = client()

    try:
        response = monster_client.get_response(
            model='sdxl-base',
            data={
                'prompt': prompt,
                'negprompt': 'unreal, fake, meme, joke, disfigured, poor quality, bad, ugly',
                'samples': 1,
                'steps': 40,
                'aspect_ratio': 'square',
                'guidance_scale': 8.5
            }
        )
        image_list = monster_client.wait_and_get_result(response['process_id'], timeout=200)
        return image_list['output'][0]  # Return the first image URL
    except Exception as e:
        return str(e)

# Flask route to handle AI image generation
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    image_url = imagen(prompt)
    if image_url:
        return jsonify({'image_url': image_url})
    else:
        return jsonify({'error': 'Failed to generate image'}), 500

# Render the index.html using Streamlit
def render_html():
    with open("index.html", 'r') as file:
        html_content = file.read()
    # Use Streamlit's HTML component to render the content
    components.html(html_content, height=800, scrolling=True)

# Main Streamlit application logic
if __name__ == "__main__":
    # Render the HTML interface
    render_html()
    
    # Start the Flask app
    app.run(port=8501)
