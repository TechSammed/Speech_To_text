# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:13:25 2025

@author: samme
"""

from fastapi import FastAPI, File, UploadFile
import speech_recognition as sr
import os

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, Render!"}
    
@app.post("/speech-to-text/")
async def speech_to_text(audio_file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    
    # Save the uploaded file temporarily
    temp_audio_path = f"temp_{audio_file.filename}"
    with open(temp_audio_path, "wb") as f:
        f.write(await audio_file.read())

    try:
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return {"transcription": text}
    except sr.UnknownValueError:
        return {"error": "Could not understand the audio"}
    except sr.RequestError as e:
        return {"error": f"API unavailable: {e}"}
    finally:
        os.remove(temp_audio_path)  # Clean up

