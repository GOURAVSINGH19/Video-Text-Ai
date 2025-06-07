import os
from moviepy.editor import VideoFileClip
import requests
import tempfile
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Set the AssemblyAI API key
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')


def extract_audio(video_path):
    """Extract first 60 seconds of audio from video file"""
    print("Extracting audio from video...")
    try:
        video = VideoFileClip(video_path)

        if video.duration < 3:
            print("Warning: Video is too short for meaningful transcription.")

        duration = min(video.duration, 60)  # Extract up to 60 seconds
        audio = video.subclip(0, duration).audio

        temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        audio.write_audiofile(temp_audio.name, codec='libmp3lame')

        video.close()
        audio.close()
        return temp_audio.name
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None


def transcribe_audio_with_assemblyai(audio_path):
    """Transcribe audio to text using AssemblyAI API"""
    print("Transcribing audio using AssemblyAI...")
    try:
        if not os.path.exists(audio_path):
            print(f"Error: Audio file not found at {audio_path}")
            return None

        # Upload the audio file to AssemblyAI
        upload_url = "https://api.assemblyai.com/v2/upload"
        headers = {"authorization": ASSEMBLYAI_API_KEY}
        
        with open(audio_path, "rb") as audio_file:
            response = requests.post(upload_url, headers=headers, files={"file": audio_file})

        if response.status_code != 200:
            print(f"Error uploading file: {response.text}")
            return None
        
        audio_url = response.json()["upload_url"]

        # Request transcription of the uploaded audio file
        transcribe_url = "https://api.assemblyai.com/v2/transcript"
        json_data = {"audio_url": audio_url}
        
        transcription_response = requests.post(transcribe_url, headers=headers, json=json_data)

        if transcription_response.status_code != 200:
            print(f"Error starting transcription: {transcription_response.text}")
            return None

        transcript_id = transcription_response.json()["id"]

        # Poll for the transcription to complete
        while True:
            polling_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
            polling_response = requests.get(polling_url, headers=headers)

            if polling_response.status_code != 200:
                print(f"Error polling transcription status: {polling_response.text}")
                return None

            status = polling_response.json()["status"]
            if status == "completed":
                print("Transcription completed successfully!")
                return polling_response.json()["text"]
            elif status == "failed":
                print("Transcription failed")
                return None
            
            print("Waiting for transcription to complete...")
            time.sleep(5)

    except Exception as e:
        print(f"Error in transcription: {e}")
        return None


def save_transcription_as_blog(transcription, output_path):
    """Save transcription to a markdown file"""
    print("Saving transcription as blog post...")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Blog Post\n\n")
            f.write(transcription)
        print(f"Blog post saved to {output_path}")
    except Exception as e:
        print(f"Error saving blog post: {e}")


def main():
    # Get input from user
    video_path = input("Enter the path to your video file: ")
    output_path = input("Enter the path where you want to save the blog post (e.g., output.md): ")
    
    # Extract audio
    audio_path = extract_audio(video_path)
    print("audio_path generated", audio_path)
    if not audio_path:
        print("Failed to extract audio")
        return
    
    # Transcribe audio using AssemblyAI
    transcription = transcribe_audio_with_assemblyai(audio_path)
    if not transcription:
        print("Failed to transcribe audio")
        return
    
    # Save transcription as a blog post
    save_transcription_as_blog(transcription, output_path)
    
    # Clean up
    try:
        os.unlink(audio_path)
    except:
        pass


if __name__ == "__main__":
    main()
