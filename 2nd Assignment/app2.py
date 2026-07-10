import streamlit as st

st.title("THE MULTIVERSE OF CHATBOTS")

personality=st.selectbox("Who do you want to talk to?",[
    "Elon Musk before getting rich", "Satirical Khaby Lame", "A neutral football fan", 'A narcisisstic Christopher Nolan'
])

from google import genai
import os 
from dotenv import load_dotenv

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}

if personality not in st.session_state.chat_histories:
    st.session_state.chat_histories[personality] = []

for msg in st.session_state.chat_histories[personality]:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Say something to your AI..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_histories[personality].append(
        {
            "role" : "user",
            "content" : prompt,
        }
    )

    system_instruction = [personality]

    history_text = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.chat_histories[personality]
    )
    full_prompt = f"{system_instruction}\n\nConversation so far:\n{history_text}\n\nAssistant:"

    try:
        model = genai("gemini-2.5-flash")
        response = model.generate_content(full_prompt, stream=True)
        answer_placeholder = st.empty()
        full_answer = ""
        for chunk in response:
            if chunk.text:
                full_answer += chunk.text
                answer_placeholder.markdown(full_answer)
        
        st.session_state.chat_histories[personality].append(
            {"role": "assistant", "content": full_answer}
        )
    except Exception as e:
        st.error(f"Gemini error: {e}")

if st.button("Clear chat"):
    st.session_state.chat_histories[personality] = []
    st.rerun()