import os
import streamlit as st
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("API_KEY")
    if not api_key:
        st.error("`API_KEY` environment variable not set.")
        st.stop()
    return genai.Client(api_key=api_key)

st.title("AI DIGITAL WELLBEING DASHBOARD")
st.write("Analyze your digital wellbeing data with CSV upload or manual entry.")

uploaded_df = None
uploaded_file = st.file_uploader(
    "Upload CSV with App Name, Category, Minutes Used",
    type=["csv"],
)
if uploaded_file:
    try:
        uploaded_df = pd.read_csv(uploaded_file)
        uploaded_df["Minutes Used"] = pd.to_numeric(uploaded_df["Minutes Used"], errors="coerce").fillna(0)
    except Exception as error:
        st.error(f"CSV error: {error}")
        uploaded_df = None

categories = [
    "Social Media",
    "Education",
    "Coding",
    "Entertainment",
    "Productivity",
    "Communication",
    "Music",
    "Shopping",
    "Finance",
]

if "rows" not in st.session_state:
    st.session_state.rows = 1

if st.button("Add Another App"):
    st.session_state.rows += 1

with st.form("screen_time"):
    app_names = []
    app_categories = []
    app_minutes = []

    for i in range(st.session_state.rows):
        st.subheader(f"App {i+1}")
        app_names.append(st.text_input("App Name", key=f"app_{i}"))
        app_categories.append(st.selectbox("Category", categories, key=f"category_{i}"))
        app_minutes.append(st.number_input("Minutes Used", min_value=0, step=15, key=f"minutes_{i}"))

    user_question = st.text_area(
        "Ask Gemini a question about this data",
        help="Optional. Leave blank for a general Gemini summary.",
    )

    if st.form_submit_button("ANALYZE"):
        if uploaded_df is not None:
            df = uploaded_df.copy()
        else:
            df = pd.DataFrame(
                {
                    "App Name": app_names,
                    "Category": app_categories,
                    "Minutes Used": app_minutes,
                }
            )
            df = df[df["App Name"].str.strip() != ""]

        if df.empty:
            st.warning("No data to analyze.")
        else:
            st.dataframe(df)
            total = int(df["Minutes Used"].sum())
            average = round(df["Minutes Used"].mean(), 1)
            maximum = int(df["Minutes Used"].max())

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Minutes", total)
            col2.metric("Average Minutes", average)
            col3.metric("Max Minutes", maximum)

            col1, col2, col3 = st.columns(3)
            col1.metric("Most Used App", df.loc[df["Minutes Used"].idxmax(), "App Name"])
            col2.metric(
                "Top Category",
                df.groupby("Category")["Minutes Used"].sum().idxmax(),
            )
            col3.metric("Least Used App", df.loc[df["Minutes Used"].idxmin(), "App Name"])

            st.subheader("Minutes Used by App")
            st.bar_chart(df.set_index("App Name")["Minutes Used"])

            if genai is not None:
                prompt = (
                    f"Analyze the following screen time data and summarize the user's app habits:\n\n"
                    f"{df.to_string(index=False)}\n\n"
                )
                if user_question:
                    prompt += f"User question: {user_question}\n\n"
                prompt += (
                    "Describe patterns, trends, and recommendations for better digital wellbeing."
                )

                with st.spinner("Generating Gemini insights..."):
                    response = genai.Client.responses.create(model="gemini-2.5-flash", input=prompt)
                answer = getattr(response, "output_text", None) or str(response)
                st.subheader("Gemini Insights")
                st.write(answer)
            else:
                st.info("Gemini insights are unavailable.")
    