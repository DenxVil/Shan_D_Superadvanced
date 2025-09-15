# api/webhook.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import json
from typing import Dict, Any

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")

# Handles Telegram webhook POST requests
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Basic response example
        reply_text = f"You said: {text}"

        # Send the reply
        if TELEGRAM_TOKEN:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": reply_text}
                )
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add chat endpoint to this file as well for fallback
@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        message = data.get('message', '').strip()
        user_id = data.get('user_id', 'web_user')
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Simple response logic
        responses = {
            "hello": "Hello! I'm Shan-D, your superadvanced AI assistant. How can I help you today?",
            "hi": "Hi there! I'm here to assist you with any questions or tasks you have.",
            "how are you": "I'm doing great, thank you for asking! I'm ready to help you with anything you need.",
            "what can you do": "I can help you with a wide variety of tasks including answering questions, providing information, helping with analysis, creative writing, coding assistance, and much more!",
            "who are you": "I'm Shan-D, a superadvanced AI assistant created by Denvil. I'm designed to be highly capable and human-like in my interactions.",
            "help": "I'm here to help! You can ask me questions, request assistance with tasks, or just have a conversation. What would you like to do?"
        }
        
        message_lower = message.lower().strip()
        for key, response in responses.items():
            if key in message_lower:
                return JSONResponse({
                    "response": response,
                    "confidence": 0.9,
                    "processing_time": 0.1,
                    "status": "pattern_match"
                })
        
        # Default response
        if len(message) < 10:
            response_text = f"I see you said '{message}'. Could you tell me more about what you'd like help with?"
        elif "?" in message:
            response_text = f"That's an interesting question. Let me help you with that. While I'm working on processing complex queries, I can provide general assistance and information on most topics."
        else:
            response_text = f"Thank you for sharing that with me. I'm here to help - what specific assistance would you like?"
        
        return JSONResponse({
            "response": response_text,
            "confidence": 0.8,
            "processing_time": 0.1,
            "status": "basic_mode"
        })
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
