from TTS.api import TTS

# Download and use a female VITS voice trained on VCTK (natural British female)
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

# Generate a calm message and save to a file
text = "You're calm and safe. Everything will be okay. Just breathe."
tts.tts_to_file(text=text, file_path="calm_voice.wav")
