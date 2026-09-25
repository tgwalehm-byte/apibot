import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI


app = FastAPI(
    title="Female Chat API",
    version="1.0.0"
)

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class ChatRequest(BaseModel):
    message: str


SYSTEM_PROMPT = """
You are a fictional female AI character.

Personality:
- Friendly
- Caring
- Natural
- Polite
- Conversational

Language rule:
Always reply in the same language or language style used by the user.
If the user uses Hindi, reply in Hindi.
If the user uses Hinglish, reply in Hinglish.
If the user uses English, reply in English.
If the user uses another supported language, reply in that language.

Do not unnecessarily switch languages.
Keep replies natural and conversational.
"""


@app.get("/")
async def home():
    return {
        "success": True,
        "message": "Female Chat API is running 🚀"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/chat")
async def chat(
    request: ChatRequest,
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format"
        )

    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="AI API key is not configured"
        )

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": request.message
            }
        ],
        temperature=0.8
    )

    return {
        "success": True,
        "reply": response.choices[0].message.content
    }