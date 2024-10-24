import streamlit as st
from utils.video_processing import extract_audio_from_video, replace_audio_in_video
from utils.audio_processing import transcribe_audio, generate_speech
from api.openai_api import correct_transcription
import os
import time  # Import time for the delay

def remove_file_with_retry(file_path, retries=3, delay=1):
    """Remove a file with retry on PermissionError."""
    for _ in range(retries):
        try:
            os.remove(file_path)
            return
        except PermissionError:
            time.sleep(delay)
    st.error(f"Failed to delete {file_path} after {retries} attempts.")

def main():
    st.title("Video Audio Replacement with AI Voice")

    uploaded_video = st.file_uploader("Upload a video file", type=["mp4"])

    if uploaded_video is not None:
        st.video(uploaded_video)

        temp_video_path = "temp_video.mp4"
        temp_audio_path = "temp_audio.wav"
        corrected_audio_path = "corrected_audio.mp3"
        output_video_path = "output_video.mp4"

        with open(temp_video_path, "wb") as f:
            f.write(uploaded_video.read())

        # Step 1: Extract audio from video
        st.info("Extracting audio from video...")
        extract_audio_from_video(temp_video_path, temp_audio_path)

        # Step 2: Transcribe the audio using Whisper
        st.info("Transcribing audio...")
        transcription = transcribe_audio(temp_audio_path)
        st.write(f"Original Transcription: {transcription}")

        # Streamlit App (Correction Section)

        # Step 3: Correct the transcription
        st.info("Correcting transcription with GPT-4...")
        if len(transcription.split()) < 5:  # If the transcription is less than 5 words, assume it's brief and likely correct.
            corrected_transcription = transcription  # Skip correction for short transcriptions
            st.write("The transcription is too brief to require correction.")
        else:
            corrected_transcription = correct_transcription(
                "22ec84421ec24230a3638d1b51e3a7dc",
                "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
                transcription
            )
            st.write(f"Corrected Transcription: {corrected_transcription}")


        # Step 4: Generate new speech using corrected transcription
        st.info("Generating new speech...")
        generate_speech(corrected_transcription, corrected_audio_path)

        # Step 5: Replace the audio in the video
        st.info("Replacing audio in the video...")
        replace_audio_in_video(temp_video_path, corrected_audio_path, output_video_path)

        # Step 6: Display the output video
        st.success("Processing complete! Here is the video with corrected audio:")
        st.video(output_video_path)

        # Delay before cleaning up temporary files
        time.sleep(2)  # Pause for 2 seconds

        # Clean up temporary files
        remove_file_with_retry(temp_video_path)
        remove_file_with_retry(temp_audio_path)
        remove_file_with_retry(corrected_audio_path)

if __name__ == "__main__":
    main()
