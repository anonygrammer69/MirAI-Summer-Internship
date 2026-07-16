# 🎨 AI Image Studio

An AI-powered image generation application built with Streamlit and Pollinations AI. Users can generate stunning AI images from text prompts, customize image dimensions, apply artistic styles, enhance prompts automatically, and generate random creative images using the Surprise Me feature.

---

## 🚀 Features

### 🖼️ AI Image Generation
- Generate images from text prompts
- Powered by Pollinations AI

### 🎨 Art Styles
Choose from multiple styles:

- Realistic
- Anime
- Cyberpunk
- Fantasy
- Digital Art

### 📏 Custom Image Dimensions
- Adjustable Width Slider
- Adjustable Height Slider
- Supports multiple image resolutions

### ✨ Magic Enhance
Improve image quality automatically by enhancing prompts with:

- Masterpiece quality
- 8K resolution
- Highly detailed rendering
- ArtStation trending style
- Unreal Engine 5 rendering

### 🎲 Surprise Me
Generate images instantly using random creative prompts.

Examples:

- An astronaut floating through the atmosphere of Jupiter
- A cyberpunk-themed visualisation of our world, 100 years from now
- A 8k, ultra-realistic picture of the Earth, from the ISS
- The Indian national football team winning the FIFA World Cup 2030
- A visualisation of Narendra Modi and Giorgio Meloni on a date in a Gondola, in the canals of Venice

### 📥 Download Images
- Download generated images as PNG files
- Dynamic file naming based on selected art style

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Requests
- Pollinations AI API

---

## 📂 Project Structure

```text
AI_IMAGE_STUDIO/
│
├── app.py
├── requirements.txt
├── README.md
└── .env (optional)
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI_IMAGE_STUDIO.git
cd AI_IMAGE_STUDIO
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🎯 Assignment 4 Features Implemented

### ✅ Task 1: Width & Height Sliders Fixed

Image dimensions are now passed to the Pollinations AI URL:

```python
url = f"https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}"
```

### ✅ Task 2: Download File Extension Fixed

Images download correctly as PNG files:

```python
file_name=f"{art_style}_image.png"
```

### ✅ Task 3: Magic Enhance Toggle

Automatically enhances prompts with:

```text
masterpiece,
8k resolution,
highly detailed,
trending on artstation,
unreal engine 5 render
```

### ✅ Task 4: Surprise Me Feature

Generates images using randomly selected creative prompts.

---

## 📸 Application Features

### Sidebar Settings

- Magic Enhance Toggle
- Width Slider
- Height Slider
- Art Style Selection

### Main Interface

- Prompt Input
- Generate Image Button
- Surprise Me Button
- Generated Image Preview
- Download Image Button

---

## 🎯 Use Cases

- Digital Art Creation
- Concept Art Generation
- Game Asset Inspiration
- AI Art Experimentation
- Creative Content Generation
- Social Media Graphics

---

## 🔮 Future Enhancements

- Image History
- Image Gallery
- AI Prompt Suggestions
- Negative Prompt Support
- Multiple Image Generation
- Image Upscaling
- User Authentication

---

## 👨‍💻 Author

**Lohit T**

LinkedIn:
https://www.linkedin.com/in/lohit-thinakaran-228b80302/

---

## 📄 License

This project was developed as part of the **MirAI School of Technology – Virtual Summer Internship 2026 (AI Builder Track)** and is intended for educational and learning purposes.