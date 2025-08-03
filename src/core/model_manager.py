"""
ⵢɧαɳ-Đ - Ultra-Enhanced AI Brain with Complete Learning Integration
Created by: ◉Ɗєиνιℓ 

"""


import asyncio
import aiohttp
import json
import logging
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
from contextlib import asynccontextmanager

class ModelType(Enum):
    REASONING = "reasoning"
    CONVERSATION = "conversation"
    MULTIMODAL = "multimodal"
    FAST_RESPONSE = "fast_response"
    SPECIALIZED = "specialized"

@dataclass
class ModelConfig:
    name: str
    api_endpoint: str
    api_key: str
    max_tokens: int
    temperature: float
    model_type: ModelType
    cost_per_token: float
    max_context: int

class AdvancedModelManager:
    def __init__(self, config: Dict):
        self.config = config
        self.models = self._initialize_models()
        self.session_pool = None
        self.performance_metrics = {}
        
    def _initialize_models(self) -> Dict[ModelType, ModelConfig]:
        """Initialize model configurations from config"""
        return {
            ModelType.REASONING: ModelConfig(
                name="gpt-4-turbo",
                api_endpoint="https://api.openai.com/v1/chat/completions",
                api_key=self.config.get('openai_api_key', ''),
                max_tokens=4096,
                temperature=0.1,
                model_type=ModelType.REASONING,
                cost_per_token=0.00003,
                max_context=128000
            ),
            ModelType.CONVERSATION: ModelConfig(
                name="claude-3-5-sonnet-20241022",
                api_endpoint="https://api.anthropic.com/v1/messages",
                api_key=self.config.get('anthropic_api_key', ''),
                max_tokens=4096,
                temperature=0.7,
                model_type=ModelType.CONVERSATION,
                cost_per_token=0.00003,
                max_context=200000
            ),
            ModelType.MULTIMODAL: ModelConfig(
                name="gemini-pro-vision",
                api_endpoint="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent",
                api_key=self.config.get('google_api_key', ''),
                max_tokens=8192,
                temperature=0.5,
                model_type=ModelType.MULTIMODAL,
                cost_per_token=0.000075,
                max_context=1000000
            ),
            ModelType.FAST_RESPONSE: ModelConfig(
                name="gpt-3.5-turbo",
                api_endpoint="https://api.openai.com/v1/chat/completions",
                api_key=self.config.get('openai_api_key', ''),
                max_tokens=1024,
                temperature=0.8,
                model_type=ModelType.FAST_RESPONSE,
                cost_per_token=0.0000015,
                max_context=16000
            )
        }
        
    async def initialize(self):
        """Initialize connection pool for optimal performance"""
        connector = aiohttp.TCPConnector(
            limit=self.config.get('max_concurrent_requests', 100),
            keepalive_timeout=30,
            enable_cleanup_closed=True,
            limit_per_host=20
        )
        
        timeout = aiohttp.ClientTimeout(
            total=self.config.get('request_timeout', 60), 
            connect=10
        )
        self.session_pool = async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
    
    async def select_optimal_model(self, query: str, context: Dict, requirements: Dict) -> ModelConfig:
        """Intelligently select the best model based on query characteristics"""
        
        # Analyze query complexity
        complexity_score = self._analyze_complexity(query)
        
        # Check for multimodal content
        has_media = self._check_media_content(context)
        
        # Determine urgency
        is_urgent = requirements.get('urgent', False)
        
        # Select model based on analysis
        if has_media:
            return self.models[ModelType.MULTIMODAL]
        elif complexity_score > 0.8:
            return self.models[ModelType.REASONING]
        elif is_urgent:
            return self.models[ModelType.FAST_RESPONSE]
        else:
            return self.models[ModelType.CONVERSATION]
    
    def _analyze_complexity(self, query: str) -> float:
        """Analyze query complexity to determine appropriate model"""
        complexity_indicators = [
            'analyze', 'calculate', 'solve', 'explain why', 'compare',
            'step by step', 'reasoning', 'logic', 'proof', 'algorithm'
        ]
        
        query_lower = query.lower()
        matches = sum(1 for indicator in complexity_indicators if indicator in query_lower)
        return min(matches / len(complexity_indicators), 1.0)
    
    def _check_media_content(self, context: Dict) -> bool:
        """Check if context contains media content"""
        return any(key in context for key in ['image', 'video', 'audio', 'file'])
    
    async def generate_response(self, query: str, context: Dict, requirements: Dict = None) -> Dict:
        """Generate AI response using optimal model selection"""
        if requirements is None:
            requirements = {}
            
        try:
            model = await self.select_optimal_model(query, context, requirements)
            
            start_time = time.time()
            response = await self._call_model_api(model, query, context)
            response_time = time.time() - start_time
            
            # Track performance metrics
            self._update_metrics(model, response_time, len(response.get('content', '')))
            
            return {
                'content': response.get('content', ''),
                'model_used': model.name,
                'response_time': response_time,
                'tokens_used': response.get('tokens_used', 0),
                'cost': response.get('tokens_used', 0) * model.cost_per_token
            }
            
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            raise
    
    async def _call_model_api(self, model: ModelConfig, query: str, context: Dict) -> Dict:
        """Make API call to specific model"""
        
        if model.model_type == ModelType.CONVERSATION and "claude" in model.name:
            return await self._call_anthropic_api(model, query, context)
        elif "gemini" in model.name:
            return await self._call_google_api(model, query, context)
        else:
            return await self._call_openai_api(model, query, context)
    
    async def _call_openai_api(self, model: ModelConfig, query: str, context: Dict) -> Dict:
        """Call OpenAI API"""
        headers = {
            "Authorization": f"Bearer {model.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = self._build_openai_messages(query, context)
        
        payload = {
            "model": model.name,
            "messages": messages,
            "max_tokens": model.max_tokens,
            "temperature": model.temperature
        }
        
        async with self.session_pool.post(model.api_endpoint, headers=headers, json=payload) as response:
            result = await response.json()
            
            return {
                'content': result['choices'][0]['message']['content'],
                'tokens_used': result['usage']['total_tokens']
            }
    
    async def _call_anthropic_api(self, model: ModelConfig, query: str, context: Dict) -> Dict:
        """Call Anthropic Claude API"""
        headers = {
            "x-api-key": model.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": model.name,
            "max_tokens": model.max_tokens,
            "temperature": model.temperature,
            "messages": [{"role": "user", "content": query}]
        }
        
        async with self.session_pool.post(model.api_endpoint, headers=headers, json=payload) as response:
            result = await response.json()
            
            return {
                'content': result['content'][0]['text'],
                'tokens_used': result['usage']['input_tokens'] + result['usage']['output_tokens']
            }
    
    async def _call_google_api(self, model: ModelConfig, query: str, context: Dict) -> Dict:
        """Call Google Gemini API"""
        headers = {
            "Content-Type": "application/json"
        }
        
        url = f"{model.api_endpoint}?key={model.api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": query}]}],
            "generationConfig": {
                "temperature": model.temperature,
                "maxOutputTokens": model.max_tokens
            }
        }
        
        async with self.session_pool.post(url, headers=headers, json=payload) as response:
            result = await response.json()
            
            return {
                'content': result['candidates'][0]['content']['parts'][0]['text'],
                'tokens_used': result.get('usageMetadata', {}).get('totalTokenCount', 0)
            }
    
    def _build_openai_messages(self, query: str, context: Dict) -> List[Dict]:
        """Build message array for OpenAI API"""
        messages = []
        
        if context.get('system_prompt'):
            messages.append({"role": "system", "content": context['system_prompt']})
        
        if context.get('conversation_history'):
            messages.extend(context['conversation_history'])
        
        messages.append({"role": "user", "content": query})
        
        return messages
    
    def _update_metrics(self, model: ModelConfig, response_time: float, response_length: int):
        """Update performance metrics for model optimization"""
        model_name = model.name
        
        if model_name not in self.performance_metrics:
            self.performance_metrics[model_name] = {
                'total_calls': 0,
                'avg_response_time': 0,
                'avg_response_length': 0,
                'total_cost': 0
            }
        
        metrics = self.performance_metrics[model_name]
        metrics['total_calls'] += 1
        metrics['avg_response_time'] = (
            metrics['avg_response_time'] * (metrics['total_calls'] - 1) + response_time
        ) / metrics['total_calls']
        metrics['avg_response_length'] = (
            metrics['avg_response_length'] * (metrics['total_calls'] - 1) + response_length
        ) / metrics['total_calls']
        metrics['total_cost'] += response_length * model.cost_per_token
    
    async def close(self):
        """Clean up resources"""
        if self.session_pool:
            await self.session_pool.close()
