import streamlit as st
import pandas as pd
import io
import os
from gtts import gTTS, gTTSError
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# ----------------- Page Setup -----------------
st.set_page_config(
    page_title="AI Training Module",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center;'>AI-Enabled Sustainability Training</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Select a topic to explore safety and sustainability practices using AI explanations, audio, and quizzes.</p>", unsafe_allow_html=True)

# ----------------- Load Environment -----------------
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# ----------------- Topic Data -----------------
topics = {
    "Machine Safety": {
        "video_url": "https://www.youtube.com/watch?v=WQMAazVc4KY",
        "quiz": [
            {"question": "What is the first step before using a machine?", "options": ["Read the manual", "Turn it on", "Check social media"], "answer": "Read the manual"},
            {"question": "Why is PPE important?", "options": ["It looks cool", "It protects from injury", "It’s optional"], "answer": "It protects from injury"}
        ]
    },
    "Water Conservation": {
        "video_url": "https://youtu.be/QLOGvbSrIDk?feature=shared",
        "quiz": [
            {"question": "What is one way to conserve water?", "options": ["Leave the tap running", "Use low-flow faucets", "Take longer showers"], "answer": "Use low-flow faucets"},
            {"question": "Why is water conservation important?", "options": ["For fun", "To save money and resources", "To waste less time"], "answer": "To save money and resources"}
        ]
    },
    "Electricity Safety": {
        "video_url": "https://youtu.be/zRHtJLFJf78?si=OXvehg3QGyiuaXEd",
        "quiz": [
            {"question": "Which of these saves energy?", "options": ["Leaving lights on", "Using LED bulbs", "Watching TV all day"], "answer": "Using LED bulbs"},
            {"question": "Why should we reduce electricity use?", "options": ["To lower costs and emissions", "To charge phones faster", "To avoid paying taxes"], "answer": "To lower costs and emissions"}
        ]
    },
    "Plantation": {
        "video_url": "https://youtu.be/4soBIwz4eMU?si=mtLpwDhPloRC7A5n",
        "quiz": [
            {"question": "Why is tree plantation important?", "options": ["It decorates the street", "It reduces pollution and improves air quality", "It increases traffic"], "answer": "It reduces pollution and improves air quality"},
            {"question": "Which of these activities supports plantation?", "options": ["Cutting trees for space", "Organizing a tree-planting drive", "Burning leaves"], "answer": "Organizing a tree-planting drive"}
        ]
    },
    "Sustainability": {
        "video_url": "https://youtu.be/OT3gsCbCKdI?si=yWRJ5lBrFnwpgR9B",
        "quiz": [
            {"question": "What does sustainability mean in the workplace?", "options": ["Using resources wisely to protect the future", "Working overtime every day", "Throwing everything in the trash"], "answer": "Using resources wisely to protect the future"},
            {"question": "Which of these is a sustainable practice?", "options": ["Using single-use plastics", "Printing unnecessary documents", "Recycling and reducing waste"], "answer": "Recycling and reducing waste"}
        ]
    }
}

# ----------------- HuggingFace LLM Client -----------------
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HF_TOKEN,
    provider="novita"
)

def generate_explanation(topic):
    try:
        prompt = f"Write a simple 100-word explanation for office employees about the topic '{topic}'. Focus on workplace safety and sustainability."
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Failed to generate explanation: {e}"

def generate_tts_memory(text):
    try:
        tts = gTTS(text)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp.read()
    except gTTSError as e:
        print(f"Error with gTTS: {e}")
        return None

# ----------------- Sidebar: Topic Selection -----------------
st.sidebar.title("📚 Training Topics")
topic = st.sidebar.selectbox("🎓 Choose a Topic", list(topics.keys()))

# ----------------- Main UI -----------------
if topic:
    st.markdown(f"### Topic: {topic}")

    col1, col2 = st.columns(2)
    with col1:
        generate = st.button("✨ Generate Explanation & Audio")
    with col2:
        show_quiz = st.button("📝 Take Quiz")

    if generate:
        ai_explanation = generate_explanation(topic)
        st.markdown("#### 📖 AI Explanation")
        st.write(ai_explanation)

        audio_bytes = generate_tts_memory(ai_explanation)
        if audio_bytes:
            st.markdown("#### 🔊 Listen to the Explanation")
            st.audio(audio_bytes, format="audio/mp3")

        st.markdown("#### 📺 Watch Topic Video")
        st.video(topics[topic]["video_url"])

    if show_quiz:
        st.markdown("### 🧪 Quick Quiz")
        with st.form("quiz_form"):
            score = 0
            user_answers = []
            for idx, q in enumerate(topics[topic]["quiz"]):
                answer = st.radio(q["question"], q["options"], key=idx)
                user_answers.append(answer)
            submit = st.form_submit_button("Submit Quiz")

        if submit:
            for i, q in enumerate(topics[topic]["quiz"]):
                if user_answers[i] == q["answer"]:
                    score += 1

            st.success(f"✅ You scored {score}/{len(topics[topic]['quiz'])}")
            if score < len(topics[topic]["quiz"]):
                st.info("📌 Please review the explanation above and try again.")
            else:
                st.balloons()

            # Save quiz score
            df = pd.DataFrame([{"topic": topic, "score": score}])
            try:
                old = pd.read_csv("results.csv")
                df = pd.concat([old, df], ignore_index=True)
            except FileNotFoundError:
                pass
            df.to_csv("results.csv", index=False)

# ----------------- Footer -----------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2025 · Developed by Kainat · AI-Powered Learning</p>",
    unsafe_allow_html=True
)
