#!/usr/bin/env python3
"""
Chat API Endpoint for Shan_D_Superadvanced Web Interface
Provides /api/chat endpoint for web frontend communication
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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

def get_chat_response(message: str, user_id: str = "web_user") -> Dict[str, Any]:
    """Generate chat response based on message content"""
    
    try:
        # Predefined responses for common inputs
        responses = {
            "hello": "Hello! I'm Shan-D, your superadvanced AI assistant. How can I help you today?",
            "hi": "Hi there! I'm here to assist you with any questions or tasks you have.",
            "how are you": "I'm doing great, thank you for asking! I'm ready to help you with anything you need.",
            "what can you do": "I can help you with a wide variety of tasks including answering questions, providing information, helping with analysis, creative writing, coding assistance, and much more!",
            "who are you": "I'm Shan-D, a superadvanced AI assistant created by Denvil. I'm designed to be highly capable and human-like in my interactions.",
            "help": "I'm here to help! You can ask me questions, request assistance with tasks, or just have a conversation. What would you like to do?"
        }
        
        # Check for pattern matches
        message_lower = message.lower().strip()
        for key, response in responses.items():
            if key in message_lower:
                return {
                    "response": response,
                    "confidence": 0.9,
                    "processing_time": 0.1,
                    "status": "pattern_match"
                }
        
        # Generate contextual response
        if len(message) < 10:
            response_text = f"I see you said '{message}'. Could you tell me more about what you'd like help with?"
        elif "?" in message:
            response_text = f"That's an interesting question. Let me help you with that. While I'm working on processing complex queries, I can provide general assistance and information on most topics."
        else:
            response_text = f"Thank you for sharing that with me. I'm here to help - what specific assistance would you like?"
        
        return {
            "response": response_text,
            "confidence": 0.8,
            "processing_time": 0.1,
            "status": "contextual_response"
        }
        
    except Exception as e:
        return {
            "response": "Hello! I'm Shan-D, your AI assistant. I'm experiencing some technical issues but I'm still here to help you. Please let me know what you need assistance with!",
            "confidence": 0.7,
            "processing_time": 0.0,
            "status": "error_fallback",
            "error": str(e)
        }

@app.post("/chat")
async def chat_endpoint(request: Request):
    """Handle chat requests from the web interface"""
    
    try:
        data = await request.json()
        message = data.get('message', '').strip()
        user_id = data.get('user_id', 'web_user')
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        response = get_chat_response(message, user_id)
        return JSONResponse(response)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/chat")
async def chat_info():
    """Provide information about the chat endpoint"""
    return JSONResponse({
        "service": "Shan-D Chat API",
        "version": "1.0.0",
        "description": "Chat with Shan-D AI Assistant",
        "usage": "POST to this endpoint with JSON: {'message': 'your message', 'user_id': 'optional_user_id'}"
    })

# For compatibility with different deployment methods
async def main(request):
    """Main handler for serverless deployment"""
    
    if request.method == "POST":
        return await chat_endpoint(request)
    elif request.method == "GET":
        return await chat_info()
    else:
        raise HTTPException(status_code=405, detail="Method not allowed")

# Export for Vercel
handler = main

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)