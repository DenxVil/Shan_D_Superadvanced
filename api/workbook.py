# api/webhook.py
from fastapi import FastAPI, Request
import os
import httpx

app = FastAPI()
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

# Handles Telegram webhook POST requests
@app.post("/webhook")
async def telegram_webhook(request: Request):
    update = await request.json()
    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")

    # Basic response example
    reply_text = f"You said: {text}"

    # Send the reply
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply_text}
        )
    return {"ok": True}
