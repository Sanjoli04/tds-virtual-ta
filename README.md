# 🧠 Virtual TA Assistant – AI-Powered Q&A System
- An intelligent Question-Answering system built with FastAPI that allows users to ask questions via text or image. It uses OCR to extract text from images,          generates embeddings with OpenAI’s text-embedding-3-small, and responds with context-aware answers using gpt-4o-mini. This project implements Retrieval-Augmented   Generation (RAG) with a local SQLite database for document chunk search.
###🔧 Features
1. ✍️ Ask questions via text or image
2. 🖼️ Image OCR support using Tesseract
3. 📚 Retrieval using embedding similarity search
4. 🤖 Contextual response generation using OpenAI GPT models
5. ⚡ Supports form-data and JSON API requests
6. 📦 SQLite used as a lightweight chunk store
7. ☁️ Deployable on Vercel or Render

### 🚀 Tech Stack
- FastAPI
- Tesseract OCR (Pillow, pytesseract)
- OpenAI (via AIProxy)
- scikit-learn – cosine similarity
- SQLite – document chunk embeddings
- Base64 image handling
- CORS-enabled API

### 📦 API Usage
- #### Endpoint: POST /api
   - Send your question and optionally an image. The assistant will extract context and generate an answer.

### 📄 JSON Example
```json
{
  "question": "What is the use of DuckDB?",
  "image": "<base64-image-string-optional>"
}
```
### 📋 Form-data Example
| Field    | Type         | Description                  |
|----------|--------------|------------------------------|
| question | `str`        | Your question                |
| image    | `UploadFile` | Optional image (PNG/JPG)     |


### ✅ How It Works
1. Accepts input (question + optional image)
2. OCR processes image → extracts text (if image present)
3. Text is embedded using `text-embedding-3-small`
4. Top similar chunks from SQLite are retrieved
5. `gpt-4o-mini` generates final response with context

### 🧪 Example Output
```vbnet
Q: What is Ollama used for?
A: Ollama is a tool to run LLMs locally. It can be used in place of cloud models...
Sources: ["Ollama - Local LLMs", "TDS Docs"]
```
### 🧭 Deployment
* #### Works with:

    - ✅ Render (via render.yaml)

    - ✅ Vercel (vercel.json for FastAPI with Python runtime)
