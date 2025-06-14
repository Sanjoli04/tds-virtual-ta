# VirtualTA Knowledge Base API Usage Guide

## Quick Setup

### 1. Prerequisites
- Python 3.7+
- ngrok account (free at https://ngrok.com)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the project root:
```
API_KEY=your_api_key_here
```

### 4. Start the Server
**Option A: Using the batch file (Windows)**
```bash
start_server.bat
```

**Option B: Using Python directly**
```bash
python deploy.py
```

### 5. Deploy with ngrok
In a separate terminal, run:
```bash
# Install ngrok if you haven't already
# Download from https://ngrok.com/download

# Start ngrok tunnel
ngrok http 8000
```

Your API will be available at the ngrok URL (e.g., `https://abc123.ngrok.io`)

## API Endpoints

### 1. Query Endpoint
**POST** `/query`

Query the knowledge base with text and optional image.

**Request Body:**
```json
{
    "question": "Your question here",
    "image": "base64_encoded_image_optional"
}
```

**Response:**
```json
{
    "answer": "Generated answer based on the knowledge base",
    "links": [
        {
            "url": "https://source1.com",
            "text": "Source description"
        }
    ]
}
```

### 2. Health Check
**GET** `/health`

Check if the API is running and database is accessible.

**Response:**
```json
{
    "status": "healthy",
    "database": "connected",
    "api_key_set": true,
    "discourse_chunks": 1234,
    "markdown_chunks": 567,
    "discourse_embeddings": 1234,
    "markdown_embeddings": 567
}
```

### 3. Web Interface
**GET** `/`

Access the web interface at the root URL.

### 4. API Documentation
**GET** `/docs`

Interactive API documentation (Swagger UI).

## Usage Examples

### Python Example
```python
import requests
import json

# Replace with your ngrok URL
BASE_URL = "https://your-ngrok-url.ngrok.io"

def query_api(question, image_base64=None):
    url = f"{BASE_URL}/query"
    payload = {
        "question": question,
        "image": image_base64  # Optional
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# Example usage
result = query_api("What is machine learning?")
print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['links'])} links found")
```

### JavaScript/Node.js Example
```javascript
const axios = require('axios');

const BASE_URL = 'https://your-ngrok-url.ngrok.io';

async function queryAPI(question, imageBase64 = null) {
    try {
        const response = await axios.post(`${BASE_URL}/query`, {
            question: question,
            image: imageBase64
        });
        
        return response.data;
    } catch (error) {
        console.error('Error querying API:', error.response?.data || error.message);
        throw error;
    }
}

// Example usage
queryAPI("Explain neural networks")
    .then(result => {
        console.log("Answer:", result.answer);
        console.log("Sources:", result.links.length);
    });
```

### cURL Example
```bash
# Text-only query
curl -X POST "https://your-ngrok-url.ngrok.io/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is artificial intelligence?"
     }'

# Health check
curl "https://your-ngrok-url.ngrok.io/health"
```

### Frontend JavaScript Example
```html
<!DOCTYPE html>
<html>
<head>
    <title>VirtualTA API Test</title>
</head>
<body>
    <input type="text" id="question" placeholder="Ask a question...">
    <button onclick="askQuestion()">Ask</button>
    <div id="result"></div>

    <script>
        const API_BASE = 'https://your-ngrok-url.ngrok.io';
        
        async function askQuestion() {
            const question = document.getElementById('question').value;
            const resultDiv = document.getElementById('result');
            
            try {
                const response = await fetch(`${API_BASE}/query`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question })
                });
                
                const result = await response.json();
                
                resultDiv.innerHTML = `
                    <h3>Answer:</h3>
                    <p>${result.answer}</p>
                    <h3>Sources:</h3>
                    <ul>
                        ${result.links.map(link => 
                            `<li><a href="${link.url}" target="_blank">${link.text}</a></li>`
                        ).join('')}
                    </ul>
                `;
            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
```

## Image Upload Example

To send an image with your query, encode it as base64:

### Python with Image
```python
import base64
import requests

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Encode the image
image_base64 = encode_image("path/to/your/image.jpg")

# Query with image
result = query_api(
    question="What do you see in this image?",
    image_base64=image_base64
)
```

### JavaScript with Image Upload
```javascript
function encodeImageFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            const base64 = reader.result.split(',')[1]; // Remove data:image/jpeg;base64, prefix
            resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Usage in form submission
document.getElementById('imageInput').addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file) {
        const imageBase64 = await encodeImageFile(file);
        // Now use imageBase64 in your API call
    }
});
```

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success
- **500**: Internal server error
- **422**: Validation error (invalid request format)

Example error response:
```json
{
    "error": "API_KEY environment variable not set"
}
```

## Rate Limiting

The API uses the OpenAI embedding service through aipipe.org. If you encounter rate limits:

1. The API automatically retries with exponential backoff
2. Consider adding delays between requests in your client
3. Monitor the logs for rate limit messages

## Troubleshooting

### Common Issues

1. **"API_KEY environment variable not set"**
   - Create a `.env` file with your API key
   - Restart the server after adding the key

2. **Database connection errors**
   - Ensure `knowledge_base.db` exists in the project directory
   - Check file permissions

3. **Empty responses**
   - Check if the database has embeddings (`/health` endpoint)
   - Ensure your question is relevant to the knowledge base content

4. **ngrok tunnel issues**
   - Make sure ngrok is authenticated: `ngrok authtoken YOUR_TOKEN`
   - Try a different port if 8000 is busy

### Getting Help

- Check the `/health` endpoint to verify system status
- View logs in the terminal where the server is running
- Use the `/docs` endpoint for interactive API testing 