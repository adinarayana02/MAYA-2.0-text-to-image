from flask import Flask, request, jsonify, send_file
import os
import requests
from monsterapi import client
from io import BytesIO

app = Flask(__name__)

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
        imageList = monster_client.wait_and_get_result(response['process_id'], timeout=200)
        image_url = imageList['output'][0]  # Returning the first image URL
        return image_url
    except Exception as e:
        return str(e)

def fetch_image(image_url):
    """Fetch the image from the URL and return as a BytesIO object."""
    response = requests.get(image_url)
    return BytesIO(response.content)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    image_url = imagen(prompt)
    if 'http' in image_url:  # simple check to see if the URL seems valid
        image_bytes = fetch_image(image_url)
        return send_file(
            image_bytes,
            mimetype='image/png',
            as_attachment=True,
            attachment_filename='generated_image.png'
        )
    else:
        return jsonify({'error': image_url}), 500

if __name__ == '__main__':
    app.run(debug=True)
