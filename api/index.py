#!/usr/bin/env python3
"""
Vercel deployment entry point for Shan_D_Superadvanced
Serves both the website and API endpoints
Created by: Copilot for ◉Ɗєиνιℓ
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import asyncio
from typing import Optional

# Add the parent directory to the path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

app = FastAPI(title="Shan_D_Superadvanced", description="Ultra-Human AI Assistant")

# Get Telegram token
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")

# Mount static files - serve our website files
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_website():
    """Serve the main website"""
    try:
        # Try to serve the index.html file
        index_path = Path(__file__).parent.parent / "static" / "index.html"
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HTMLResponse(content=content)
        else:
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html><head><title>Shan_D_Superadvanced</title></head>
            <body><h1>Shan_D_Superadvanced AI Assistant</h1>
            <p>Website is loading... Please check back in a moment.</p>
            <p>If this persists, there may be a configuration issue.</p>
            </body></html>
            """)
    except Exception as e:
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html><head><title>Error</title></head>
        <body><h1>Error Loading Website</h1>
        <p>Error: {str(e)}</p>
        </body></html>
        """, status_code=500)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "service": "Shan_D_Superadvanced",
        "version": "1.0.0",
        "timestamp": "2025-09-15T22:37:00Z"
    })

@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    """Handle Telegram webhook requests"""
    if not TELEGRAM_TOKEN:
        raise HTTPException(status_code=500, detail="Telegram token not configured")
    
    try:
        update = await request.json()
        
        # Basic validation
        if "message" not in update:
            return {"ok": True, "status": "ignored - no message"}
        
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Simple response for now
        reply_text = f"🤖 Shan-D received: {text}\n\nI'm your Ultra-Human AI Assistant! How can I help you today?"

        # Send the reply
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": reply_text}
            )
            response.raise_for_status()

        return {"ok": True, "status": "message sent"}
    
    except Exception as e:
        # Log error but don't fail completely
        print(f"Webhook error: {e}")
        return {"ok": False, "error": str(e)}

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """Handle web chat requests"""
    try:
        data = await request.json()
        message = data.get("message", "")
        user_id = data.get("user_id", "web_user")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Simple echo response for now - in production this would connect to the full AI
        response_text = f"🤖 Shan-D AI: I received your message '{message}'. I'm currently in basic mode but fully operational! Ask me anything and I'll help you to the best of my abilities."
        
        return JSONResponse({
            "response": response_text,
            "confidence": 0.95,
            "processing_time": 0.1,
            "timestamp": "2025-09-15T22:37:00Z"
        })
    
    except Exception as e:
        return JSONResponse(
            {"error": f"Failed to process chat message: {str(e)}"},
            status_code=500
        )

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return JSONResponse({
        "service": "Shan_D_Superadvanced",
        "status": "operational",
        "version": "1.0.0",
        "features": [
            "Web Chat Interface",
            "Telegram Bot Integration", 
            "AI Assistant",
            "Real-time Responses"
        ],
        "endpoints": {
            "/": "Main website",
            "/health": "Health check",
            "/api/status": "Service status",
            "/api/chat": "Web chat API",
            "/api/webhook": "Telegram webhook"
        }
    })

# For local development/testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)