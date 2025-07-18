# AI-Enabled Sustainability Training Module

This Streamlit app is an interactive training tool designed to educate users on workplace sustainability and safety topics using AI-generated content, quizzes, and explainer videos. It provides both text and audio explanations.

## Features

- Topic-wise training on:
  - Machine Safety
  - Water Conservation
  - Electricity Safety
  - Plantation
  - Sustainability
- 🧠 AI-generated explanations using Mistral model (via HuggingFace)
- 🎧 Text-to-speech support (via gTTS)
- 📺 Educational YouTube video for each topic
- 📝 Multiple-choice quizzes with instant scoring

##  Setup Instructions

```bash
# Clone the repo
git clone https://github.com/Kainattkhan/AI-Training-Module.git
cd AI-Training-Module

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set Hugging Face token in .env
echo HF_TOKEN=your_huggingface_token > .env

# Run the app
streamlit run app.py
