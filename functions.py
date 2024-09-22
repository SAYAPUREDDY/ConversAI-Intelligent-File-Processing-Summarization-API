
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

def text_from_pdf(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def text_to_meta(text):
    documents = []
    if text:
        documents.append(Document(page_content=text, metadata={"title": "document"}))
    return documents

def conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = create_stuff_documents_chain(model, prompt)
    return chain

def process_genai_files(action, question=None, file_paths=None):
    responses = []
    for file_path in file_paths:
        if action == "summarize":
            prompt = "Summarize the content of this file."
        else:
            prompt = f"Based on the context answer this question: {question}"
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        genai_file = genai.upload_file(path=file_path)
        
        while genai_file.state.name == "PROCESSING":
            print('.', end='', flush=True)
            time.sleep(10)
            genai_file = genai.get_file(genai_file.name)
        
        if genai_file.state.name == "FAILED":
            raise ValueError("File processing failed.")

        response = model.generate_content(
            [
                prompt,
                genai_file
            ]
        )
        responses.append(response.text)
    
    return responses