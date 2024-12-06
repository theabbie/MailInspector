from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class EmailRequest(BaseModel):
    content: str

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.post("/analyze")
async def analyze_email(email: EmailRequest):
    # Use LLM to analyze email
    analysis = await analyze_with_llm(email.content)
    return analysis

async def analyze_with_llm(content: str):
    # Implement your LLM prompt here
    prompt = f"""
    Analyze the following email and provide:
    1. Overall tone (formal/informal/urgent)
    2. Key action items (if any)
    3. A brief suggested response

    Email: {content}
    """
    # Call LLM API
    client = anthropic.Client(ANTHROPIC_API_KEY)
    response = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=300,
        model="claude-2"
    )
    return response.completion

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))