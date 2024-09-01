import streamlit as st
import os
import requests
from monsterapi import client
from io import BytesIO

# Function to generate image using Monster API
def imagen(prompt):
    os.environ['MONSTER_API_KEY'] = os.getenv('MONSTERAI_API_KEY')
    monster_client = client()

    try:
        with st.spinner('Generating image...'):
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
            st.success("Image generated successfully!")
            return imageList['output'][0]  # Returning the first image URL
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to fetch image from URL
def fetch_image(image_url):
    """Fetch the image from the URL and return as a BytesIO object."""
    response = requests.get(image_url)
    return BytesIO(response.content)

# Set up the Streamlit app layout
st.set_page_config(
    page_title="AI Image Generator",
    page_icon='🤖',
    layout='centered'
)

# Custom HTML and CSS
st.markdown("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Image Generator | LUNA AI</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Roboto:wght@400;500&display=swap" rel="stylesheet">
    <!-- Font Awesome for Icons -->
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    <style>
        /* Reset CSS */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* Variables for colors and fonts */
        :root {
            --primary-color: #2980b9;
            --secondary-color: #34495e;
            --light-color: #ecf0f1;
            --dark-color: #2c3e50;
            --font-primary: 'Roboto', sans-serif;
            --font-secondary: 'Montserrat', sans-serif;
        }

        /* Global Styles */
        body {
            font-family: var(--font-primary);
            color: var(--dark-color);
            line-height: 1.6;
        }

        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px 0;
        }

        /* Header Styles */
        .header {
            background-color: var(--secondary-color);
            color: var(--light-color);
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .header .container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo h1 {
            font-family: var(--font-secondary);
            font-size: 1.8em;
        }

        .nav ul {
            list-style: none;
            display: flex;
            align-items: center;
        }

        .nav ul li {
            margin-left: 20px;
        }

        .nav ul li a {
            color: var(--light-color);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .nav ul li a:hover {
            color: var(--primary-color);
        }

        .cta .btn {
            background-color: var(--primary-color);
            color: #fff;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }

        .cta .btn:hover {
            background-color: #1f6391;
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #6fb1fc 0%, #4364f7 100%);
            color: #fff;
            padding: 100px 0;
        }

        .hero .container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
        }

        .hero-content {
            flex: 1;
            min-width: 300px;
        }

        .hero-content h2 {
            font-family: var(--font-secondary);
            font-size: 2.5em;
            margin-bottom: 20px;
        }

        .hero-content p {
            font-size: 1.2em;
            margin-bottom: 30px;
        }

        .btn-primary {
            background-color: #fff;
            color: var(--primary-color);
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease, color 0.3s ease;
            text-decoration: none;
        }

        .btn-primary:hover {
            background-color: var(--primary-color);
            color: #fff;
        }

        .hero-image {
            flex: 1;
            min-width: 300px;
            text-align: center;
        }

        .hero-image img {
            max-width: 100%;
            height: auto;
            border-radius: 15px;
        }

        /* Features Section */
        .features {
            background-color: #f4f4f9;
            padding: 60px 0;
            text-align: center;
        }

        .features h2 {
            font-family: var(--font-secondary);
            font-size: 2em;
            margin-bottom: 40px;
        }

        .features-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }

        .feature-item {
            flex: 1 1 220px;
            background-color: #fff;
            padding: 30px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .feature-item:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.2);
        }

        .feature-item i {
            font-size: 2.5em;
            color: var(--primary-color);
            margin-bottom: 15px;
        }

        .feature-item h3 {
            font-family: var(--font-secondary);
            margin-bottom: 15px;
        }

        .feature-item p {
            font-size: 1em;
            color: #7f8c8d;
        }

        /* How It Works Section */
        .how-it-works {
            padding: 60px 0;
            text-align: center;
        }

        .how-it-works h2 {
            font-family: var(--font-secondary);
            font-size: 2em;
            margin-bottom: 40px;
        }

        .steps {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }

        .step {
            flex: 1 1 250px;
            background-color: #fff;
            padding: 30px 20px;
            border-radius: 10px;
            position: relative;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .step:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.2);
        }

        .step-number {
            background-color: var(--primary-color);
            color: #fff;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: 700;
            position: absolute;
            top: -25px;
            left: calc(50% - 25px);
        }

        .step h3 {
            font-family: var(--font-secondary);
            margin-top: 40px;
            margin-bottom: 15px;
        }

        .step p {
            font-size: 1em;
            color: #7f8c8d;
        }

        /* Footer Styles */
        .footer {
            background-color: var(--secondary-color);
            color: var(--light-color);
            padding: 30px 0;
        }

        .footer .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .footer p {
            margin-bottom: 15px;
        }

        .footer a {
            color: var(--light-color);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .footer a:hover {
            color: var(--primary-color);
        }

        .footer .social-icons {
            margin-top: 15px;
        }

        .footer .social-icons a {
            color: var(--light-color);
            margin: 0 10px;
            font-size: 1.5em;
            transition: color 0.3s ease;
        }

        .footer .social-icons a:hover {
            color: var(--primary-color);
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">
                <h1>LUNA AI</h1>
            </div>
            <nav class="nav">
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Features</a></li>
                    <li><a href="#">Pricing</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </nav>
            <div class="cta">
                <a href="#" class="btn">Get Started</a>
            </div>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <h2>Generate Stunning Images with AI</h2>
                <p>Experience the power of artificial intelligence in creating beautiful and unique images tailored to your needs.</p>
                <a href="#" class="btn-primary">Start Creating</a>
            </div>
            <div class="hero-image">
                <img src="https://via.placeholder.com/600x400" alt="AI Image">
            </div>
        </div>
    </section>

    <section class="features">
        <div class="container">
            <h2>Features</h2>
            <div class="features-grid">
                <div class="feature-item">
                    <i class="fas fa-paint-brush"></i>
                    <h3>Creative Freedom</h3>
                    <p>Generate images based on your creative ideas and explore new possibilities.</p>
                </div>
                <div class="feature-item">
                    <i class="fas fa-cogs"></i>
                    <h3>Customizable</h3>
                    <p>Adjust parameters and styles to fit your specific requirements and preferences.</p>
                </div>
                <div class="feature-item">
                    <i class="fas fa-share-alt"></i>
                    <h3>Easy Sharing</h3>
                    <p>Share your creations easily with built-in sharing options and social media integration.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="how-it-works">
        <div class="container">
            <h2>How It Works</h2>
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>Enter Your Prompt</h3>
                    <p>Provide a detailed description of the image you want to generate.</p>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>Generate Image</h3>
                    <p>Our AI processes your prompt and generates a stunning image.</p>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>Download & Share</h3>
                    <p>Download your image or share it directly from the platform.</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 LUNA AI. All rights reserved.</p>
            <p>Follow us on:</p>
            <div class="social-icons">
                <a href="#"><i class="fab fa-facebook-f"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-linkedin-in"></i></a>
                <a href="#"><i class="fab fa-instagram"></i></a>
            </div>
        </div>
    </footer>
</body>
</html>
""", unsafe_allow_html=True)

# Form for user input
with st.form(key='input_form'):
    prompt = st.text_area("Enter your image prompt:", height=150)
    submit_button = st.form_submit_button(label="Generate Image")

if submit_button:
    image_url = imagen(prompt)
    if image_url:
        image_stream = fetch_image(image_url)
        st.image(image_stream, caption="Generated Image", use_column_width=True)
