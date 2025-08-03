"""
Enhanced LLM Handler for Shan-D
Created by: ◉Ɗєиνιℓ 👨‍💻
Handles multiple LLM providers with intelligent routing
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
import openai
import anthropic
from groq import Groq
from configs.config import Config

logger = logging.getLogger(__name__)

class EnhancedLLMHandler:
    """Enhanced LLM handler with multiple provider support"""
    
    def __init__(self):
        self.config = Config()
        self.openai_client = None
        self.anthropic_client = None
        self.groq_client = None
        
        self._initialize_clients()
        logger.info("🤖 EnhancedLLMHandler initialized by ◉Ɗєиνιℓ")
    
    def _initialize_clients(self):
        """Initialize available LLM clients"""
        if self.config.OPENAI_API_KEY:
            self.openai_client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
        
        if self.config.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.AsyncAnthropic(api_key=self.config.ANTHROPIC_API_KEY)
        
        if self.config.GROQ_API_KEY:
            self.groq_client = Groq(api_key=self.config.GROQ_API_KEY)
    
    async def generate_response(
        self, 
        messages: List[Dict], 
        context: Dict,
        provider: str = "auto"
    ) -> str:
        """Generate response using best available provider"""
        
        if provider == "auto":
            provider = self._choose_best_provider(context)
        
        try:
            if provider == "openai" and self.openai_client:
                return await self._generate_openai_response(messages, context)
            elif provider == "anthropic" and self.anthropic_client:
                return await self._generate_anthropic_response(messages, context)
            elif provider == "groq" and self.groq_client:
                return await self._generate_groq_response(messages, context)
            else:
                return await self._generate_fallback_response(messages, context)
        
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return "I'm having trouble generating a response right now. Can you try again?"
    
    def _choose_best_provider(self, context: Dict) -> str:
        """Choose best LLM provider based on context"""
        # Simple provider selection logic
        if context.get("conversation_type") == "creative":
            return "anthropic" if self.anthropic_client else "openai"
        elif context.get("requires_speed"):
            return "groq" if self.groq_client else "openai"
        else:
            return "openai" if self.openai_client else "anthropic"
    
    async def _generate_openai_response(self, messages: List[Dict], context: Dict) -> str:
        """Generate response using OpenAI"""
        response = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    async def _generate_anthropic_response(self, messages: List[Dict], context: Dict) -> str:
        """Generate response using Anthropic Claude"""
        # Convert messages format for Claude
        system_message = "You are Shan-D, an ultra-human AI assistant created by ◉Ɗєиνιℓ (🤖)."
        user_message = messages[-1]["content"] if messages else ""
        
        response = await self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            system=system_message,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.content[0].text
    
    async def _generate_groq_response(self, messages: List[Dict], context: Dict) -> str:
        """Generate response using Groq"""
        # Note: Groq client might need to be adapted for async
        # This is a simplified implementation
        return "Groq response generation not fully implemented yet."
    
    async def _generate_fallback_response(self, messages: List[Dict], context: Dict) -> str:
        """Fallback response when no LLM is available"""
        fallbacks = [
            "I'm here to chat! What would you like to talk about?",
            "Hey! I'm ready to help. What's on your mind?",
            "I'm Shan-D, your AI assistant. How can I help you today?"
        ]
        return fallbacks[0]
