from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import time
import tempfile
from typing import List
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import uvicorn
from functions import text_from_pdf,text_to_meta,conversational_chain,process_genai_files
app = FastAPI()

uploaded_files = {}

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    session_id = len(uploaded_files)
    session_files = {"pdf": [], "audio": [], "video": []}
    
    for file in files:
        if file.content_type == "application/pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(await file.read())
                session_files["pdf"].append(tmp_file.name)
        
        elif file.content_type in ["audio/wav", "audio/mp3"]:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.' + file.filename.split('.')[-1]) as tmp_file:
                tmp_file.write(await file.read())
                session_files["audio"].append(tmp_file.name)
        
        elif file.content_type in ["video/mp4", "video/mkv", "video/avi"]:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.' + file.filename.split('.')[-1]) as tmp_file:
                tmp_file.write(await file.read())
                session_files["video"].append(tmp_file.name)
        
        else:
            return JSONResponse(status_code=400, content={"message": "Invalid file type. Only PDF, audio, and video files are allowed."})
    
    uploaded_files[session_id] = session_files
    return {"session_id": session_id}

@app.post("/summarize/")
async def summarize_files(session_id: int = Form(...)):
    if session_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="Session not found. Please upload files first.")

    session_data = uploaded_files[session_id]
    pdf_summaries = []
    audio_summaries = []
    video_summaries = []

    if session_data["pdf"]:
        pdf_paths = session_data["pdf"]
        pdf_text = text_from_pdf(pdf_paths)
        pdf_summaries.append("PDF Summary: " + pdf_text)  # Replace with actual summarization logic if available
    
    if session_data["audio"]:
        audio_paths = session_data["audio"]
        audio_summaries = process_genai_files(action="summarize", file_paths=audio_paths)
    
    if session_data["video"]:
        video_paths = session_data["video"]
        video_summaries = process_genai_files(action="summarize", file_paths=video_paths)

    if not pdf_summaries and not audio_summaries and not video_summaries:
        return JSONResponse(status_code=400, content={"message": "No files to summarize in this session."})

    return {
        "pdf_summaries": pdf_summaries,
        "audio_summaries": audio_summaries,
        "video_summaries": video_summaries
    }


@app.post("/ask-question/")
async def ask_question(session_id: int = Form(...), question: str = Form(...)):
    if session_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="Session not found. Please upload files first.")

    session_data = uploaded_files[session_id]

    responses = []

    
    if session_data["pdf"]:
        pdf_paths = session_data["pdf"]
        text = text_from_pdf(pdf_paths)
        docs = text_to_meta(text)
        chain = conversational_chain()
        response_pdf = chain.invoke({"context": docs, "question": question})
        responses.append(response_pdf)
    
    
    if session_data["audio"]:
        audio_paths = session_data["audio"]
        response_audio = process_genai_files(action="answer", question=question, file_paths=audio_paths)
        responses.extend(response_audio)
    
    if session_data["video"]:
        video_paths = session_data["video"]
        response_video = process_genai_files(action="answer", question=question, file_paths=video_paths)
        responses.extend(response_video)

    if not responses:
        return JSONResponse(status_code=400, content={"message": "No files to process in this session."})

    return {"responses": responses}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
