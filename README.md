# 🧠 TDS Virtual TA Assistant

A smart **TA (Teaching Assistant) helper** built using FastAPI that accepts **questions** and optionally an **image**, and returns an intelligent response using context-aware embeddings. Powered by **AIProxy** and OpenAI models like `gpt-4o-mini`.

---

## ✨ Features

- 🔍 Accepts user **questions** via JSON or HTML form
- 🖼️ Supports **image input** (base64 encoded)
- 🧾 Uses **OCR** (Tesseract) to extract text from images
- 🧠 Generates **embeddings** using `text-embedding-3-small`
- 🔗 Ranks related **document chunks** using cosine similarity
- 🤖 Generates smart, context-based answers using `gpt-4o-mini`
- 🌐 CORS-enabled for easy frontend access

---

## 🛠️ Tech Stack

- **FastAPI** (Python)
- **OpenAI-compatible API** via [AIProxy](https://github.com/sanand0/aipipe)
- **Tesseract OCR** for image text extraction
- **SQLite** for embedding chunk storage
- **scikit-learn** for similarity ranking

---

## 🚀 How It Works

1. User sends a **question** and optionally an **image**.
2. If image is provided:
   - Text is extracted via OCR.
   - This text is appended to the question for context.
3. The combined input is converted into an **embedding**.
4. Embedding is matched against local `chunks.db` for top relevant content.
5. Final answer is generated using `gpt-4o-mini` with the top chunks as context.

---

## 📦 API Endpoints

### `POST /api`

Send a **question** with optional base64-encoded **image**.

#### 🧾 JSON Request Format
```json
{
  "question": "What does this diagram explain?",
  "image": "<optional base64-encoded image string>"
}
```