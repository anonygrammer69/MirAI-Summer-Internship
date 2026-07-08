import streamlit as st

#TITLE
st.title("The Identity Echo Interface")

#INSTRUCTIONS
st.write("Enter your name and message below, then click the Transmit button.")

#INPUTS
user_name = st.text_input("Enter your Name")
user_message = st.text_input("Enter your Message")

#BUTTON
if st.button("Transmit"):


    if user_name.strip() == "":
        st.error("Please provide your name.")


    elif user_message.strip() == "":
        st.warning("Please type a message to transmit.")


    else:
        st.success("Transmission successful!")
        st.success(f"**Greetings, {user_name}.**")
        st.success(f"**We received your message:- {user_message}**")

        character_count = len(user_message)
        token_count = character_count / 4

        st.info(
            f"System Check: Your message will consume approximately "
            f"{token_count:.2f} tokens from our context window."
        )