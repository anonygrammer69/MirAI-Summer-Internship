# Assignment 5: Multi-Modal Visual Novel

Capstone mini-project for the MirAI School of Technology Virtual Summer Internship 2026, AI Builder Track.

This project is a Streamlit-based "Choose Your Own Adventure" visual novel engine. It uses Gemini for stateful story generation, Pollinations for visual scene generation, Python JSON parsing for structured AI output, dynamic Streamlit buttons for player choices, and gTTS for browser-playable narration.

## Demo

[**Watch the Demo Video**](https://drive.google.com/file/d/1Q4ubhtJmAMTvjfBO7quLRGax0uPHgqMa/view?usp=sharing)
## Features

- Stateful visual novel flow using `st.session_state`
- Cached Gemini client using `@st.cache_resource`
- Sidebar story configuration for genre and art style
- Strict Gemini JSON response format:
  - `story_text`
  - `image_prompt`
  - `options`
- JSON parsing with Python's built-in `json` library
- Dynamic choice buttons generated from Gemini's `options` list
- Pollinations image generation from the AI-produced `image_prompt`
- Text-to-speech narration with `gTTS`
- Streamlit audio playback with `st.audio()`
- Graceful failure handling with `try...except` and `st.toast()`

## Project Structure

```text
assignment-5/
+-- app.py
+-- requirements.txt
+-- README.md
+-- src/
    +-- __init__.py
    +-- audio_service.py
    +-- gemini_client.py
    +-- prompt.py
```

## Environment Variables

Create a `.env` file in the repository root with:

```env
API_KEY=your_gemini_api_key
GTTS_KEY=optional_value
```

`API_KEY` is required for Gemini. `GTTS_KEY` is read by `audio_service.py` because it was part of the assignment setup, but the `gTTS` library does not require an API key.

Do not submit or share your `.env` file.

## Installation

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m pip install -r assignment-5\requirements.txt
```

If you are not using the existing virtual environment, create and activate one first:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r assignment-5\requirements.txt
```

## Run the App

```powershell
.\.venv\Scripts\streamlit.exe run assignment-5\app.py
```

Then open the local Streamlit URL shown in the terminal.

## How It Works

1. Choose a story genre and art style from the sidebar.
2. Enter an opening story idea.
3. Gemini returns a strict JSON object containing the next scene, image prompt, and choices.
4. The app parses the JSON into a Python dictionary.
5. The Pollinations API generates a scene image.
6. gTTS converts the story text into an MP3 narration file.
7. Streamlit renders the scene, image, audio player, and dynamic choice buttons.
8. Clicking a choice sends that exact option back to Gemini as the next player move.

## Assignment Phase Mapping

### Phase 1: Director's Cut

- `@st.cache_resource` caches the Gemini client in `get_gemini_client()`.
- The sidebar is titled `Story Settings`.
- `st.session_state` stores chat state, scene history, current scene, and scene number.

### Phase 2: Structured JSON Engine

- `src/prompt.py` instructs Gemini to return strict JSON.
- `app.py` uses `json.loads()` inside `parse_scene()` to convert Gemini text into a dictionary.

### Phase 3: Dynamic UI Generation

- `app.py` loops over `scene["options"]`.
- Each option becomes an `st.button()`.
- The clicked button text is sent back to Gemini as the next move.

### Phase 4: Multimedia Rendering and TTS

- Pollinations image generation happens in `fetch_pollinations_image()`.
- Audio generation happens in `src/audio_service.py`.
- Images are shown with `st.image()`.
- Narration is played with `st.audio()`.

### Phase 5: Graceful Failures

- Gemini, image generation, and audio generation are wrapped in `try...except`.
- Image and audio failures use `st.toast()` so the app continues without crashing.

## Submission Checklist

- Record a 60-second screen recording of the app in action.
- Capture system audio so the narration is audible.
- Show dynamic buttons changing after selecting choices.
- Submit `assignment-5/app.py` to the student portal.
- Do not submit `.env` or API keys.