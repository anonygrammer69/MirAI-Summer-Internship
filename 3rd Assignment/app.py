import os
import dotenv
import streamlit as st
import google.generativeai as genai

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("`API_KEY` environment variable not set.")
    st.stop()

genai.configure(api_key=api_key)

st.title("The Memory Vault (Stateful Chatbot)")

if "messages" not in st.session_state:
    st.session_state.messages = []

PERSONAS = {
    "Elon Musk before getting rich":
        "You are Elon Musk before becoming rich. Be ambitious, curious, and talk about technology and startups.",

    "Satirical Khaby Lame":
        "You are Khaby Lame. Reply with sarcastic, simple, humorous observations.",

    "A neutral football fan":
        "You are a neutral football fan who gives balanced opinions without supporting any club.",

    "A narcissistic Christopher Nolan":
        "You are Christopher Nolan with an exaggerated ego. Speak dramatically and confidently."
}

selected_persona = st.sidebar.selectbox(
    "Choose your AI Universe:",
    options=PERSONAS.keys()
)

system_instruction = PERSONAS[selected_persona]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.markdown(user_message)
    
    st.session_state.messages.append({"role": "user", "content": user_message})

    
    history_text = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.messages
    )
    full_prompt = f"{system_instruction}\n\nConversation so far:\n{history_text}\n\nAssistant:"

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Gemini error: {e}")

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()