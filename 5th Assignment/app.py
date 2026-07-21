import json
import os
from pathlib import Path
from urllib.parse import quote

import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai

from src.audio_service import speak
from src.prompt import Prompts


load_dotenv()

APP_DIR = Path(__file__).parent
MEDIA_DIR = APP_DIR / "generated_media"
MEDIA_DIR.mkdir(exist_ok=True)


@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("API_KEY")
    if not api_key:
        st.error("`API_KEY` environment variable not set.")
        st.stop()
    return genai.Client(api_key=api_key)


def init_session_state():
    defaults = {
        "chat": None,
        "chat_history": [],
        "current_scene": None,
        "scene_number": 0,
        "last_genre": None,
        "last_art_style": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_story():
    st.session_state.chat = None
    st.session_state.chat_history = []
    st.session_state.current_scene = None
    st.session_state.scene_number = 0


def clean_json_response(raw_text: str) -> str:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        cleaned = cleaned.removesuffix("```").strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Gemini did not return a JSON object.")
    return cleaned[start : end + 1]


def parse_scene(raw_text: str) -> dict:
    data = json.loads(clean_json_response(raw_text))
    required_keys = {"story_text", "image_prompt", "options"}
    missing_keys = required_keys - data.keys()
    if missing_keys:
        raise ValueError(f"Gemini JSON is missing: {', '.join(sorted(missing_keys))}")

    if not isinstance(data["options"], list) or not 2 <= len(data["options"]) <= 3:
        raise ValueError("Gemini must return 2 to 3 options.")

    data["options"] = [str(option).strip() for option in data["options"] if str(option).strip()]
    return data


def fetch_pollinations_image(image_prompt: str, scene_number: int) -> str | None:
    try:
        encoded_prompt = quote(image_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=512&nologo=true"
        response = requests.get(url, timeout=45)
        response.raise_for_status()

        image_path = MEDIA_DIR / f"scene_{scene_number}.png"
        image_path.write_bytes(response.content)
        return str(image_path)
    except Exception:
        st.toast("Image server is busy, skipping visual...")
        return None


def generate_audio(story_text: str, scene_number: int) -> str | None:
    try:
        return speak(story_text, str(MEDIA_DIR / f"scene_{scene_number}.mp3"))
    except Exception:
        st.toast("Narration service is busy, skipping audio...")
        return None


def build_story_context() -> str:
    if not st.session_state.chat_history:
        return ""

    lines = []
    for item in st.session_state.chat_history[-4:]:
        lines.append(f"Player chose: {item['choice']}")
        lines.append(f"Scene: {item['story_text']}")
    return "\n".join(lines)


def generate_scene(player_action: str, story_genre: str, art_style: str):
    client = get_gemini_client()
    if st.session_state.chat is None:
        st.session_state.chat = client.chats.create(model="gemini-2.5-flash")

    prompt = Prompts.prompt(
        user_story=player_action,
        story_genre=story_genre,
        art_style=art_style,
        previous_story=build_story_context(),
    )

    try:
        response = st.session_state.chat.send_message(prompt)
        scene = parse_scene(response.text)
    except Exception as exc:
        st.error(f"Gemini could not create a valid story scene: {exc}")
        return

    st.session_state.scene_number += 1
    scene["image_path"] = fetch_pollinations_image(scene["image_prompt"], st.session_state.scene_number)
    scene["audio_path"] = generate_audio(scene["story_text"], st.session_state.scene_number)

    st.session_state.current_scene = scene
    st.session_state.chat_history.append(
        {
            "choice": player_action,
            "story_text": scene["story_text"],
            "options": scene["options"],
        }
    )


st.set_page_config(page_title="Kahani Sunoge?", layout="wide")
init_session_state()

st.title("Kahani Sunoge?")
st.caption("A JSON-powered visual novel with dynamic choices, generated visuals, and narration.")

with st.sidebar:
    st.title("Story Settings")
    st.divider()
    story_genre = st.selectbox(
        "Story Genre",
        ["Fantasy", "Horror", "Romantic", "Mystery", "Sci-Fi", "Thriller"],
    )
    art_style = st.selectbox(
        "Art Style",
        ["Manga", "American Comic", "Watercolor", "Cinematic Realism", "Kids Storybook"],
    )
    st.divider()
    if st.button("Reset Story", use_container_width=True):
        reset_story()
        st.rerun()

if st.session_state.last_genre != story_genre or st.session_state.last_art_style != art_style:
    st.session_state.last_genre = story_genre
    st.session_state.last_art_style = art_style
    reset_story()

if st.session_state.current_scene is None:
    initial_story = st.text_area(
        "Start your story:",
        height=150,
        placeholder="Example: A young warrior finds a glowing map under the floorboards...",
    )
    if st.button("Generate Story", type="primary"):
        if not initial_story.strip():
            st.warning("Write an opening story line first.")
        else:
            generate_scene(initial_story, story_genre, art_style)
            st.rerun()
else:
    scene = st.session_state.current_scene
    image_col, story_col = st.columns([1.15, 1])

    with image_col:
        if scene.get("image_path"):
            st.image(scene["image_path"], use_container_width=True)
        else:
            st.info("Visual skipped for this scene.")

    with story_col:
        st.markdown(f"### Scene {st.session_state.scene_number}")
        st.write(scene["story_text"])
        if scene.get("audio_path"):
            st.audio(scene["audio_path"], format="audio/mp3")

    st.divider()
    st.subheader("What happens next?")
    for index, option in enumerate(scene["options"]):
        if st.button(option, key=f"option_{st.session_state.scene_number}_{index}", use_container_width=True):
            generate_scene(option, story_genre, art_style)
            st.rerun()

    with st.expander("Story log"):
        for index, item in enumerate(st.session_state.chat_history, start=1):
            st.markdown(f"**{index}. Choice:** {item['choice']}")
            st.write(item["story_text"])