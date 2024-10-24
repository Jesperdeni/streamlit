from moviepy.editor import VideoFileClip, AudioFileClip

def extract_audio_from_video(video_path, output_audio_path):
    """
    Extracts audio from the video file.
    """
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_audio_path)
    except Exception as e:
        print(f"Error extracting audio: {e}")

def replace_audio_in_video(video_path, new_audio_path, output_video_path):
    """
    Replaces the audio in the original video file with the AI-generated voice.
    """
    try:
        with VideoFileClip(video_path) as video:
            new_audio = AudioFileClip(new_audio_path)
            video = video.set_audio(new_audio)
            video.write_videofile(output_video_path)
    except Exception as e:
        print(f"Error replacing audio: {e}")
