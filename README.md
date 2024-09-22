# ConversAI-Intelligent-File-Processing-Summarization-API
This repository contains a FastAPI-based solution that allows users to upload PDF, audio, and video files, and then process these files for summarization or question-answering. This system leverages Google Generative AI for conversational processing and summarization tasks, enabling seamless interactions with multimedia content.

## Features

- **File Upload**: Supports uploading multiple file types, including PDFs, audio (WAV/MP3), and video (MP4/MKV/AVI).
- **PDF Summarization**: Extracts text from uploaded PDFs and summarizes the content.
- **Audio/Video Summarization**: Uses generative AI to summarize audio and video files.
- **Conversational AI**: Ask questions about the uploaded content, and the system will generate answers based on the file data.
- **Google Generative AI**: Integrated with Google Generative AI for advanced natural language processing.

## Tech Stack

- **FastAPI**: Python-based web framework for building APIs.
- **PyPDF2**: PDF processing library to extract text from PDF files.
- **Google Generative AI**: API integration for language processing, summarization, and question answering.
- **Langchain**: Framework for chaining AI models and building conversational agents.
- **Uvicorn**: ASGI server for running the FastAPI application.

## API Endpoints

### 1. Upload Files
Endpoint to upload PDF, audio, or video files.

```http
POST /upload/
```
Request:
- Form-data: Files (PDF, audio, video)
  
Response :
```json
{
  "session_id": 1
}
```
### 2. Summarize files
Generates summaries for uploaded PDF, audio, and video files within a session.
```http
POST /summarize/
```
Request:
- Form-data: session_id (integer)
  
Response:
```json
{
  "pdf_summaries": ["..."],
  "audio_summaries": ["..."],
  "video_summaries": ["..."]
}
```
### 3. Ask Questions About Uploaded Content
Allows users to ask questions related to the content of the uploaded files.
```http
POST /ask-question/
```
Request:
- Form-data: session_id (integer), question (string)
Response:
```json
{
  "responses": ["..."]
}
```
# setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/SAYAPUREDDY/ConversAI-Intelligent-File-Processing-Summarization-API.git
```
### 2. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3. Setup Environment Vairables
You need to configure the Google Generative AI API key.
```bash
export GOOGLE_API_KEY="your-google-api-key"
```
### 4. Start the application
```bash
python all_in_one.py
```
# Usage Instructions
1. Upload files using the /upload/ endpoint (PDF, audio, or video).
2. Get summaries of uploaded content by calling /summarize/ with the session ID.
3. Ask questions about the content using the /ask-question/ endpoint.










