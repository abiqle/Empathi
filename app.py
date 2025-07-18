import streamlit as st
import requests
from TTS.api import TTS
import tempfile
import os
import pygame

# Page Setup
st.set_page_config(page_title="🧘‍♀️ Empathi - AI Therapist", layout="centered")
st.title("🧘‍♀️ Empathi - Your AI Therapist")
st.write("Speak your thoughts freely. I'm here to listen and help.")

# Input from user
user_input = st.text_area("How are you feeling today?", height=150)
response_text = ""

# When Talk button is pressed
if st.button("Talk to Me") and user_input.strip():
    with st.spinner("Empathi is listening..."):
        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "mistral",
                    "messages": [{"role": "user", "content": user_input}],
                    "stream": False
                }
            )
            data = response.json()
            response_text = data["message"]["content"]
        except Exception as e:
            st.error(f"❌ Error talking to Ollama: {e}")
            st.stop()

    # Display text response immediately
    st.markdown("### 🧠 Empathi says:")
    st.success(response_text)

    # Store response in session for later speech
    st.session_state['reply'] = response_text

# Optional Speak Button AFTER response
if 'reply' in st.session_state and st.button("🔊 Speak Out Loud"):
    try:
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

        # Temp WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            audio_path = fp.name
            tts.tts_to_file(text=st.session_state['reply'], file_path=audio_path)

        # Play audio
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(audio_path)

    except Exception as e:
        st.warning(f"⚠️ Could not play voice: {e}")


st.markdown("""---""")
st.markdown(
    "<p style='text-align: center; color: gray;'>Built with ❤️ by <a href='https://github.com/abiqle' target='_blank'>Abinav</a></p>",
    unsafe_allow_html=True
)