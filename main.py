from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount templates and static directories
templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
TOKEN = os.getenv("AIPIPE_TOKEN")
BASE_URL = "https://aipipe.org/openai/v1"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
DB_PATH = "chunks.db"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Utility functions
def get_embedding(text: str):
    payload = {"model": EMBEDDING_MODEL, "input": text}
    response = requests.post(
        f"{BASE_URL}/embeddings", headers=HEADERS, json=payload, timeout=15
    )
    return response.json()["data"][0]["embedding"]

def get_top_chunks(query_embedding, top_k=3):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT metadata_json, content, embedding FROM chunks")
    rows = cur.fetchall()
    conn.close()

    scored = []
    for metadata_json, content, emb_json in rows:
        db_emb = json.loads(emb_json)
        score = cosine_similarity([query_embedding], [db_emb])[0][0]
        scored.append((score, metadata_json, content))
    return sorted(scored, key=lambda x: -x[0])[:top_k]

def generate_answer(question: str, chunks: list):
    context = "\n\n".join(c for _, _, c in chunks)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer only from the provided context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
    ]
    payload = {"model": CHAT_MODEL, "messages": messages}
    resp = requests.post(
        f"{BASE_URL}/chat/completions", headers=HEADERS, json=payload, timeout=15
    )
    return resp.json()["choices"][0]["message"]["content"]

def extract_text_from_base64(image_b64: str) -> str:
    try:
        data = base64.b64decode(image_b64)
        img = Image.open(io.BytesIO(data))
        return pytesseract.image_to_string(img)
    except Exception:
        return ""

# Combined endpoint: accepts JSON or form-data
@app.post("/api")
async def api(request: Request):
    ct = request.headers.get("content-type", "")
    question = None
    image_b64 = None

    if "application/json" in ct:
        body = await request.json()
        question = body.get("question")
        image_b64 = body.get("image")
    elif "multipart/form-data" in ct:
        form = await request.form()
        question = form.get("question")
        upload: UploadFile = form.get("image")
        if upload:
            img_bytes = await upload.read()
            image_b64 = base64.b64encode(img_bytes).decode()
    else:
        return JSONResponse({"error": "Unsupported Content-Type"}, status_code=415)

    if not question:
        return JSONResponse({"error": "Missing 'question'"}, status_code=422)

    # Build full context
    full_ctx = question
    if image_b64:
        ocr_text = extract_text_from_base64(image_b64)
        full_ctx = f"{ocr_text}\n\n{question}" if ocr_text else question

    # Retrieval
    q_emb = get_embedding(full_ctx)
    if not q_emb:
        return JSONResponse({"error": "Embedding failed"}, status_code=500)
    top = get_top_chunks(q_emb)
    ans = generate_answer(question, top)

    links = [
        {"title": json.loads(md)["title"], "url": json.loads(md).get("original_url", "")}
        for _, md, _ in top
    ]

    return {"answer": ans, "links": links}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
