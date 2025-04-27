import streamlit as st
import requests
import io
import base64
from PIL import Image
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Mandala Art Generator",
    page_icon="🔮",
    layout="centered"
)

# Title and description
st.title("✨ Black & White Mandala Art Generator")
st.write("Enter your OpenAI API key and an inspiration word to create a beautiful black and white mandala design.")

# Function to generate mandala image using DALL-E 3
def generate_mandala(api_key, prompt_word):
    # Initialize OpenAI client with user-provided API key
    client = OpenAI(api_key=api_key)
    
    # Craft a detailed prompt for the mandala
    prompt = f"""Create a detailed, intricate black and white mandala design inspired by the word '{prompt_word}'. 
    The mandala should be perfectly symmetrical, highly detailed, and contain elements that symbolize '{prompt_word}'.
    The design should be strictly monochromatic (black and white only) with no gray shades.
    Use clean, crisp lines with a focus on geometric patterns and repeating elements.
    Make the image suitable for printing and coloring."""
    
    try:
        # Generate image with DALL-E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard",
            response_format="url"
        )
        
        # Get the image URL
        image_url = response.data[0].url
        
        # Download the image
        image_response = requests.get(image_url)
        img = Image.open(io.BytesIO(image_response.content))
        
        return img
    
    except Exception as e:
        st.error(f"Error generating mandala: {str(e)}")
        return None

# Function to create a download link for the image
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">**{text}**</a>'
    return href

# Main app logic
with st.form("mandala_generator_form"):
    # API key input with password masking
    api_key = st.text_input("Enter your OpenAI API Key:", type="password", help="Your API key will not be stored and is only used for this session")
    
    # Input field for the inspiration word
    inspiration_word = st.text_input("Enter your inspiration word:", placeholder="peace, harmony, nature, etc.")
    
    # Generate button
    submit_button = st.form_submit_button("Generate Mandala")

    if submit_button:
        # Validate inputs
        if not api_key:
            st.error("Please enter your OpenAI API key.")
        elif not inspiration_word:
            st.warning("Please enter an inspiration word.")
        else:
            with st.spinner(f"Creating your '{inspiration_word}' mandala..."):
                # Call the function to generate the mandala
                mandala_image = generate_mandala(api_key, inspiration_word)
                
                if mandala_image:
                    # Display the generated image
                    st.success("Your mandala has been created!")
                    st.image(mandala_image, caption=f"Mandala inspired by '{inspiration_word}'", use_column_width=True)
                    
                    # Create download link
                    st.markdown(
                        get_image_download_link(
                            mandala_image, 
                            f"{inspiration_word}_mandala.png", 
                            "Download your mandala"
                        ), 
                        unsafe_allow_html=True
                    )
                    
                    st.write("Feel free to print it out and color it or use it for meditation and relaxation.")

# Add instructions and information
st.markdown("---")
with st.expander("How to use this app"):
    st.write("""
    1. Enter your OpenAI API key in the first text box. Your key will not be stored.
    2. Enter a single word that inspires you in the second text box.
    3. Click the 'Generate Mandala' button.
    4. Wait a few seconds while the AI creates your custom mandala.
    5. Once generated, you can download the image by clicking the download link.
    6. Print the image and use it for coloring, meditation, or decoration.
    """)

with st.expander("About OpenAI API Keys"):
    st.write("""
    To use this app, you need an OpenAI API key that has access to DALL-E 3. 
    - If you don't have an API key, you can get one from [OpenAI's platform](https://platform.openai.com/).
    - Your API key is only used for this session and is not stored anywhere.
    - Using DALL-E 3 will incur charges on your OpenAI account based on OpenAI's pricing.
    """)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and DALL-E 3")