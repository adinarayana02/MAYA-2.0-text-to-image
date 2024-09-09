import streamlit as st
import os
import requests
from monsterapi import client
from io import BytesIO

def imagen(prompt, samples):
    os.environ['MONSTER_API_KEY'] = os.getenv('MONSTERAI_API_KEY')
    monster_client = client()

    

    try:
        with st.spinner('Generating image...'):
            response = monster_client.get_response(
                model='sdxl-base',
                data={
                    'prompt':prompt,
                    'negprompt': 'unreal, fake, meme, joke, poor quality, bad, ugly',
                    'samples': samples,
                    'steps': 100,
                    'aspect_ratio': 'square',
                    'guidance_scale': 10
                }
            )
            imageList = monster_client.wait_and_get_result(response['process_id'], timeout=200)
            st.success("Images generated successfully!")
            return imageList['output']  # Returning the list of image URLs
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

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

# Custom CSS styles
st.markdown("""
    <style>
    /* General background and text colors */
    .main {
        background-color: #f4f4f9;
        color: #2c3e50;
        font-family: 'Roboto', sans-serif;
    }
    /* Header styling */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #34495e;
        padding: 15px 20px;
        color: #ecf0f1;
        border-bottom: 2px solid #2c3e50;
        flex-wrap: wrap;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .header .title {
        font-size: 1.8em;
        font-weight: 700;
        font-family: 'Montserrat', sans-serif;
    }
    .header .nav-links {
        font-size: 1.1em;
        font-weight: 500;
    }
    .header .nav-links a {
        color: #ecf0f1;
        text-decoration: none;
        margin: 0 15px;
        transition: color 0.3s ease;
    }
    .header .nav-links a:hover {
        color: #bdc3c7;
    }
    @media (max-width: 768px) {
        .header {
            flex-direction: column;
            text-align: center;
        }
        .header .nav-links {
            margin-top: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .header .nav-links a {
            margin: 5px 0;
        }
    }
    /* Footer styling */
    .footer {
        background-color: #34495e;
        color: #ecf0f1;
        padding: 20px;
        text-align: center;
        font-size: 1em;
        border-top: 2px solid #2c3e50;
        margin-top: 30px;
        box-shadow: 0 -4px 8px rgba(0,0,0,0.1);
    }
    @media (max-width: 768px) {
        .footer {
            font-size: 0.9em;
        }
    }
    /* Title */
    .css-h5rgaw {
        color: #2c3e50;
        text-align: center;
        font-size: 2.2em;
        font-weight: 700;
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 20px;
    }
    /* Caption */
    .css-18e3th9 {
        color: #7f8c8d;
        text-align: center;
        font-size: 1em;
        margin-bottom: 30px;
        font-family: 'Roboto', sans-serif;
    }
    /* Subheader (Input Prompt) */
    .css-1kyxreq {
        color: #2c3e50;
        font-size: 1.2em;
        font-weight: 500;
        font-family: 'Roboto', sans-serif;
    }
    /* Text area styling */
    .stTextArea textarea {
        background-color: #ffffff;
        color: #2c3e50;
        border: 1px solid #bdc3c7;
        padding: 10px;
        border-radius: 8px;
        font-family: 'Roboto', sans-serif;
        width: 100%;
        transition: border-color 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #2980b9;
        outline: none;
    }
    /* Button styling */
    .stButton button {
        background-color: #2980b9;
        color: #ffffff;
        border: none;
        padding: 12px 24px;
        font-size: 1em;
        border-radius: 8px;
        font-family: 'Roboto', sans-serif;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #21618c;
    }
    /* Spinner color */
    .stSpinner {
        color: #2980b9;
    }
    /* Download button styling */
    .stDownloadButton button {
        background-color: #2980b9;
        color: #ffffff;
        border: none;
        padding: 12px 24px;
        font-size: 1em;
        border-radius: 8px;
        font-family: 'Roboto', sans-serif;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stDownloadButton button:hover {
        background-color: #21618c;
    }
    /* Styling for additional content */
    .additional-content {
        text-align: center;
        margin-top: 30px;
    }
    .additional-content h3 {
        color: #2c3e50;
        font-size: 1.8em;
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 15px;
    }
    .additional-content p {
        color: #7f8c8d;
        font-size: 1em;
        font-family: 'Roboto', sans-serif;
        margin-bottom: 10px;
        line-height: 1.5;
    }
    /* Markdown styling for overall text blocks */
    .stMarkdown {
        color: #2c3e50;
        font-family: 'Roboto', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('''
    <div class="header">
        <div class="title">MAYA 2.0 AI</div>
        </div>
    </div>
''', unsafe_allow_html=True)

# Main content
st.title("AI Image Generator 🧑‍💻")
st.caption("© Adinarayana Thota")
st.caption("This is an AI Image Generator. It creates an image from scratch from a text description.")

# Create a container for the layout
with st.container():
    st.subheader("Input Prompt")
    with st.form("prompt_form", clear_on_submit=False):
        prompt = st.text_area("Enter your prompt here", height=100)
        samples = st.slider("Number of Samples", min_value=1, max_value=4, value=2)
        submit_button = st.form_submit_button(label="Generate")

    if submit_button:
        image_urls = imagen(prompt, samples)
        if image_urls:
            st.subheader("Generated Images")
            cols = st.columns(samples)
            for i, image_url in enumerate(image_urls):
                with cols[i]:
                    st.image(image_url, use_column_width=True)
                    image_bytes = fetch_image(image_url)
                    st.download_button(
                        label="Download Image",
                        data=image_bytes,
                        file_name=f"generated_image_{i+1}.png",
                        mime="image/png"
                    )
        else:
            st.error("Failed to generate images.")

    # Additional content below the generate button
    st.markdown("""
        <div class="additional-content">
            <h3>Creativity at the Speed of Your Imagination</h3>
            <p>Create beautiful variations instantly.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('''
    <div class="footer">
        <div class="footer-content">
            <p>Powered by MAYA 2.O AI</p>
            <p>Created by Adinarayana Thota ❤️|Contact us: support@lunaai.com </p>
        </div>
    </div>
''', unsafe_allow_html=True)
