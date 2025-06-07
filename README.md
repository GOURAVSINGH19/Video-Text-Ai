🎥 Video to Blog Converter
Convert video content into structured blog posts using AI.
This Python application extracts audio from video files, transcribes it to text, and uses OpenAI's GPT model to generate a well-formatted blog post in Markdown.

🚀 Features
```
🎧 Extracts audio from video files

🗣️ Transcribes speech to text using Google Speech Recognition

✨ Generates blog posts using OpenAI's GPT model

📝 Outputs blog posts in Markdown format

🔄 Tracks progress and handles errors gracefully

🧰 Prerequisites
```
Make sure you have the following before getting started:
```
Python 3.7 or higher

OpenAI API key

Internet connection (for transcription and GPT processing)

📦 Installation
Clone the repository or download the source files.

Install required Python packages:

pip install -r requirements.txt
```
Set up your API key:
Create a .env file in the project root directory and add:
```
ini
OPENAI_API_KEY=your_api_key_here

```
▶️ Usage
Run the script:
```
Edit
python video_to_blog.py
```
Follow the prompts:

Enter the path to your video file (e.g., my_video.mp4)

Enter the desired output path for the blog post (e.g., blog_output.md)

The script will:

Extract audio from the video

Transcribe the audio to text

Generate a blog post using GPT

Save the post to the specified file

🎥 Supported Video Formats
This tool supports common video file formats:
```
.mp4

.avi

.mov

.wmv

.flv

.mkv
```
⚠️ Notes
Transcription quality depends on the clarity of the video's audio.

Processing time increases with video length.

Ensure adequate disk space for temporary files.

The OpenAI API key is required for generating the blog post.

🛠️ Error Handling
The script includes checks for:

Invalid or corrupted video files

Speech recognition failures

OpenAI API connection or quota issues

File write or permission errors

If an error occurs, detailed messages will appear in the console for troubleshooting.
