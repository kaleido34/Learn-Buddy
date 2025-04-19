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
    prompt = """You are a summarizer.Create a detailed and concise summary of the provided transcript for display on a website. The summary should capture the key points, main ideas, and essential takeaways from the content. Ensure it is well-structured, easy to read, and optimized for web readability. Include the following elements:

Introduction: Briefly introduce the topic or subject of the transcript.

Main Points: Highlight the primary arguments, themes, or sections discussed.

Key Takeaways: Summarize the most important insights, conclusions, or actionable information.

Supporting Details: Include relevant examples, data, or quotes that reinforce the main points.

Conclusion: Provide a brief wrap-up or final thoughts on the content.

Ensure the summary is engaging, accurate, and tailored for a general audience while maintaining the original context and meaning of the transcript. Avoid jargon or overly complex language, and aim for a length of approximately 150–300 words, depending on the depth of the content. The summary has to be displayed on a separate website so remove the extra stars and while changing sections for e.g. intoduction to main idea. Make it start  from a new line. And also avoid words like 'this transcript is' instead start explaining in a more detialed amd refined manner """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + content)
        return response.text
    except Exception as e:
        return f"Error during summarization: {e}"

# Function to generate questions based on content using Google Gemini
def generate_questions(content):
    prompt = """"Generate a set of multiple-choice questions (MCQs) based on the provided transcript to serve as an interactive learning or engagement tool for website visitors. The questions should be clear, relevant, and designed to test comprehension of the key points, main ideas, and details from the content. Follow these guidelines:

Question Types:

Include a mix of factual, conceptual, and application-based questions.

Ensure questions cover the most important aspects of the transcript.

Structure:

Each question should have one correct answer and three plausible distractors (incorrect answers).

Avoid ambiguous or overly complex wording.

Coverage:

Distribute questions evenly across the transcript to cover all major sections or themes.

Include questions on key takeaways, supporting details, and any critical insights.

Difficulty Level:

Create a balance of easy, moderate, and challenging questions to cater to a wide audience.

Give answwer key at the end.

Output Format:

Present the questions in a clear, numbered list.

Group questions by topic or section if the transcript is lengthy.

Example:
Q1. What is the main topic discussed in the transcript?
a) Option 1
b) Option 2
c) Option 3 (Correct Answer)
d) Option 4

Generate at least 6-7 high-quality MCQs that align with the transcript's content and purpose, ensuring they are engaging and educational for website visitors..
    Each question should have the following format:
    <Question Number>: <Question Text>
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