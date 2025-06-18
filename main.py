from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
import os
import io
import requests
import json
import sqlite3
from PIL import Image
import pytesseract
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TOKEN = os.getenv("AIPIPE_TOKEN")
BASE_URL = "https://aipipe.org/openai/v1"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
DB_PATH = "chunks.db"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def get_embedding(text: str):
    payload = {"model": EMBEDDING_MODEL, "input": text}
    try:
        response = requests.post(f"{BASE_URL}/embeddings", headers=HEADERS, json=payload)
        return response.json()["data"][0]["embedding"]
    except Exception as e:
        print("Embedding error:", e)
        return None

def get_top_chunks(query_embedding, top_k=3):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT metadata_json, content, embedding FROM chunks")
    rows = cur.fetchall()
    conn.close()

    scored_chunks = []
    for metadata_json, content, embedding_json in rows:
        db_embedding = json.loads(embedding_json)
        score = cosine_similarity([query_embedding], [db_embedding])[0][0]
        scored_chunks.append((score, metadata_json, content))

    return sorted(scored_chunks, key=lambda x: -x[0])[:top_k]

def generate_answer(question: str, context_chunks: list):
    context_text = "\n\n".join(chunk for _, _, chunk in context_chunks)

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer questions based only on the provided chunks."},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion:\n{question}"}
    ]

    payload = {
        "model": CHAT_MODEL,
        "messages": messages
    }

    response = requests.post(f"{BASE_URL}/chat/completions", headers=HEADERS, json=payload)
    response_json = response.json()

    return response_json["choices"][0]["message"]["content"]

def extract_text_from_base64(image_base64: str):
    try:
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))
        return pytesseract.image_to_string(image)
    except Exception as e:
        print("OCR error:", e)
        return ""

@app.post("/api")
async def handle_request(request: Request):
    content_type = request.headers.get("content-type", "")

    question = None
    image_b64 = None

    if "application/json" in content_type:
        body = await request.json()
        question = body.get("question")
        image_b64 = body.get("image")

    elif "multipart/form-data" in content_type:
        form = await request.form()
        question = form.get("question")
        image_file = form.get("image")
        if image_file:
            image_bytes = await image_file.read()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    else:
        return JSONResponse({"error": "Unsupported content type"}, status_code=415)

    if not question:
        return JSONResponse({"error": "Missing 'question'"}, status_code=422)

    full_context = question
    if image_b64:
        extracted_text = extract_text_from_base64(image_b64)
        full_context = f"{extracted_text}\n\n{question}"

    query_embedding = get_embedding(full_context)
    if not query_embedding:
        return JSONResponse({"error": "Failed to get embedding"}, status_code=500)

    top_chunks = get_top_chunks(query_embedding)
    final_answer = generate_answer(question, top_chunks)

    return {
        "answer": final_answer,
        "source_titles": [json.loads(md)["title"] for _, md, _ in top_chunks],
        "original_urls": [json.loads(md).get("original_url") for _, md, _ in top_chunks]
    }

@app.get("/")
def home():
    return {"message": "TDS TA Assistant API running. Use POST /api with question and optional image."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
