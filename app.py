import streamlit as st
import os
import requests
from monsterapi import client
from io import BytesIO

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
        background-color: #f4f4f9;  /* Very light grey background for a clean look */
        color: #2c3e50;  /* Dark slate color for text */
        font-family: 'Roboto', sans-serif;  /* Modern and clean font */
    }
    /* Header styling */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #34495e;  /* Dark blue-grey background for header */
        padding: 15px 20px;
        color: #ecf0f1;  /* Light grey text color */
        border-bottom: 2px solid #2c3e50;  /* Slightly darker border for header */
        flex-wrap: wrap;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Light shadow for a more defined look */
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
        transition: color 0.3s ease; /* Smooth transition for link hover effect */
    }
    .header .nav-links a:hover {
        color: #bdc3c7;  /* Slightly lighter color on hover */
    }
    /* Responsive styling for navigation links */
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
        background-color: #34495e;  /* Dark blue-grey background for footer */
        color: #ecf0f1;  /* Light grey text color */
        padding: 20px;
        text-align: center;
        font-size: 1em;
        border-top: 2px solid #2c3e50;  /* Slightly darker border for footer */
        margin-top: 30px;
        box-shadow: 0 -4px 8px rgba(0,0,0,0.1); /* Light shadow for footer */
    }
    /* Responsive footer content */
    @media (max-width: 768px) {
        .footer {
            font-size: 0.9em;
        }
    }
    /* Title */
    .css-h5rgaw {
        color: #2c3e50;  /* Dark slate for title */
        text-align: center;
        font-size: 2.2em;  /* Adjusted for responsiveness */
        font-weight: 700;  /* Bolder font weight for emphasis */
        font-family: 'Montserrat', sans-serif;  /* Elegant and bold font */
        margin-bottom: 20px;
    }
    /* Caption */
    .css-18e3th9 {
        color: #7f8c8d;  /* Medium grey for the caption */
        text-align: center;
        font-size: 1em;  /* Balanced font size */
        margin-bottom: 30px;
        font-family: 'Roboto', sans-serif;  /* Consistent font */
    }
    /* Subheader (Input Prompt) */
    .css-1kyxreq {
        color: #2c3e50;  /* Dark slate for input prompt label */
        font-size: 1.2em;  /* Slightly larger font size */
        font-weight: 500;
        font-family: 'Roboto', sans-serif;
    }
    /* Text area styling */
    .stTextArea textarea {
        background-color: #ffffff;  /* White background for the text area */
        color: #2c3e50;  /* Dark slate text color */
        border: 1px solid #bdc3c7;  /* Light grey border */
        padding: 10px;  /* Consistent padding */
        border-radius: 8px;  /* Rounded corners for a modern look */
        font-family: 'Roboto', sans-serif;
        width: 100%;  /* Full width for better mobile usability */
        transition: border-color 0.3s ease; /* Smooth transition on focus */
    }
    .stTextArea textarea:focus {
        border-color: #2980b9;  /* Blue border on focus */
        outline: none;  /* Remove outline */
    }
    /* Button styling */
    .stButton button {
        background-color: #2980b9;  /* Bright blue color for the button */
        color: #ffffff;  /* White text */
        border: none;
        padding: 12px 24px;  /* Larger padding for emphasis */
        font-size: 1em;  /* Adjusted font size */
        border-radius: 8px;  /* Rounded corners */
        font-family: 'Roboto', sans-serif;
        font-weight: 600;  /* Semi-bold text for the button */
        transition: background-color 0.3s ease;  /* Smooth transition on hover */
    }
    .stButton button:hover {
        background-color: #21618c;  /* Slightly darker blue on hover */
    }
    /* Spinner color */
    .stSpinner {
        color: #2980b9;  /* Bright blue spinner */
    }
    /* Download button styling */
    .stDownloadButton button {
        background-color: #2980b9;  /* Same blue as the submit button */
        color: #ffffff;  /* White text */
        border: none;
        padding: 12px 24px;
        font-size: 1em;  /* Adjusted font size */
        border-radius: 8px;
        font-family: 'Roboto', sans-serif;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stDownloadButton button:hover {
        background-color: #21618c;  /* Slightly darker blue on hover */
    }
    /* Styling for additional content */
    .additional-content {
        text-align: center;
        margin-top: 30px;
    }
    .additional-content h3 {
        color: #2c3e50;  /* Dark slate for heading */
        font-size: 1.8em;
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 15px;
    }
    .additional-content p {
        color: #7f8c8d;  /* Medium grey for paragraphs */
        font-size: 1em;
        font-family: 'Roboto', sans-serif;
        margin-bottom: 10px;
        line-height: 1.5;
    }
    /* Markdown styling for overall text blocks */
    .stMarkdown {
        color: #2c3e50;  /* Dark slate color */
        font-family: 'Roboto', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('''
    <div class="header">
        <div class="title">LUNA AI</div>
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
        prompt = st.text_area("Enter your prompt here", height=100)  # Reduced height
        submit_button = st.form_submit_button(label="Generate")

    if submit_button:
        image_url = imagen(prompt)
        if image_url:
            st.subheader("Generated Image")
            st.image(image_url, use_column_width=True)
            
            # Add download button
            image_bytes = fetch_image(image_url)
            st.download_button(
                label="Download Image",
                data=image_bytes,
                file_name="generated_image.png",
                mime="image/png"
            )
        else:
            st.error("Failed to generate image.")

    # Additional content below the generate button
    st.markdown("""
        <div class="additional-content">
            <h3>Creativity at the Speed of Your Imagination</h3>
            <p>Create beautiful variations instantly.</p>
            <p>Generate your very own AI images from text prompts with 123RF in seconds! Watch as our advanced AI algorithms interpret your words and transform them into photorealistic visuals right before your eyes. From imaginative landscapes and abstract art to product designs and brand visuals, our AI image generator opens up a world of endless creative possibilities. No design skills are required - simply describe your desired image, and let our powerful technology do the rest. Elevate your projects with unique, attention-grabbing visuals created by you, for you, in an instant!</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('''
    <div class="footer">
        <div class="footer-content">
            <p>Powered by LUNA AI</p>
            <p>Contact us: support@lunaai.com | Created by Adinarayana Thota <a href="#" style="color: #ecf0f1; text-decoration: underline;">Social Media</a></p>
        </div>
    </div>
''', unsafe_allow_html=True)
