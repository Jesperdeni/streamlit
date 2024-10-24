import whisper
from gtts import gTTS
from pydub import AudioSegment

def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("small")  # Example of loading a smaller model
    except Exception as e:
        print("Error loading Whisper model:", str(e))
        return "Model loading error"

    # Transcribe the audio file
    result = model.transcribe(audio_path)

    # Extract the transcription text
    transcription = result['text']

    return transcription

def generate_speech(text, output_path):
    try:
        # Create a gTTS object and save the output to a file
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)

        # Convert the saved mp3 to a wav file for compatibility
        audio_segment = AudioSegment.from_mp3(output_path)
        audio_segment.export(output_path.replace('.mp3', '.wav'), format='wav')
    except Exception as e:
        print(f"Error generating speech: {e}")
        return "Speech generation error"
