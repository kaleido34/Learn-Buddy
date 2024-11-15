import os
import whisper
from youtube_transcript_api import YouTubeTranscriptApi
from PyPDF2 import PdfReader
from pytesseract import pytesseract
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load Whisper ASR model
asr_model = whisper.load_model("base")

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Content processing functions
def process_video(file_path=None, youtube_url=None):
    transcript = ""
    if file_path:
        result = asr_model.transcribe(file_path)
        transcript = result["text"]
    elif youtube_url:
        video_id = youtube_url.split("v=")[-1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
    return transcript

def process_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_image(file_path):
    image = cv2.imread(file_path)
    text = pytesseract.image_to_string(image)
    return text

# Summarization function using Google Gemini
def summarize_text(content):
    prompt = """You are a summarizer. Summarize the input text into important points within 250 words.
    Here is the input text: """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + content)
        return response.text
    except Exception as e:
        return f"Error during summarization: {e}"

# Function to generate questions based on content using Google Gemini
def generate_questions(content):
    prompt = """You are a question generator. Based on the provided text, generate multiple-choice questions with four possible answers.
    Each question should have the following format:
    Question: <Question Text>
    A) <Option A>
    B) <Option B>
    C) <Option C>
    D) <Option D>
    Here is the input text: """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + content)
        questions = response.text.strip().split("\n")
        return questions
    except Exception as e:
        return [f"Error generating questions: {e}"]

from flask import request

@app.route("/process-content", methods=["POST"])
def process_content():
    content_type = request.form.get("content_type")
    youtube_url = request.form.get("youtube_url")
    file = request.files.get("file")

    result = ""
    if content_type == "video" and file:
        # Save the uploaded file to a temporary path
        temp_path = "temp_uploaded_video.mp4"
        file.save(temp_path)
        result = process_video(file_path=temp_path)
    elif youtube_url:
        result = process_video(youtube_url=youtube_url)
    elif content_type == "pdf" and file:
        temp_path = "temp_uploaded_pdf.pdf"
        file.save(temp_path)
        result = process_pdf(file_path=temp_path)
    elif content_type == "image" and file:
        temp_path = "temp_uploaded_image.jpg"
        file.save(temp_path)
        result = process_image(file_path=temp_path)

    summary = summarize_text(result)
    questions = generate_questions(result)
    
    return jsonify({
        "transcription": result,
        "summary": summary,
        "questions": questions
    })

if __name__ == "__main__":
    app.run(debug=True)