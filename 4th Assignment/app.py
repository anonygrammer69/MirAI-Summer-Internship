from urllib.parse import quote
import random
import requests
import streamlit as st

st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨"
)

st.title("🎨 AI Image Studio")

# Sidebar Settings
st.sidebar.header("Settings")

magic_enhance = st.sidebar.checkbox(
    "✨ Enable Magic Enhance"
)

width = st.sidebar.slider(
    "Width",
    256,
    1024,
    512
)

height = st.sidebar.slider(
    "Height",
    256,
    1024,
    512
)

art_style = st.sidebar.selectbox(
    "Art Style",
    [
        "Realistic",
        "Anime",
        "Cyberpunk",
        "Fantasy",
        "Digital Art"
    ]
)

# Surprise Prompts
surprise_prompts = [
    "An astronaut floating through the atmosphere of Jupiter",
    "A cyberpunk-themed visualisation of our world, 100 years from now",
    "A 8k, ultra-realistic picture of the Earth, from the ISS",
    "The Indian national football team winning the FIFA Wrold Cup 2030",
    "A visualisation of Narendra Modi and Giorgio Meloni on a date in a Gondola, in the canals of Venice"
]

prompt = st.text_input(
    "Enter your image prompt"
)

col1, col2 = st.columns(2)

generate = col1.button("🎨 Generate Image")
surprise = col2.button("🎲 Surprise Me!")

if surprise:
    prompt = random.choice(surprise_prompts)
    st.info(f"Prompt: {prompt}")
    generate = True

if generate:

    if not prompt:
        st.warning("Enter a prompt")
        st.stop()

    full_prompt = f"{prompt}, {art_style}"

    if magic_enhance:
        full_prompt += (
            ", masterpiece, 8k resolution, "
            "highly detailed, trending on artstation, "
            "unreal engine 5 render"
        )

    encoded_prompt = quote(full_prompt)

    # Assignment Task 1
    url = (
        f"https://image.pollinations.ai/prompt/"
        f"{encoded_prompt}"
        f"?width={width}&height={height}"
    )

    st.info("Generating image...")

    response = requests.get(url)

    if response.status_code == 200:

        st.image(
            response.content,
            caption=full_prompt
        )

        # Assignment Task 2
        st.download_button(
            "📥 Download Image",
            data=response.content,
            file_name=f"{art_style}_image.png",
            mime="image/png"
        )

    else:
        st.error("Image generation failed")