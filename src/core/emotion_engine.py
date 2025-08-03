"""
Advanced Emotion Engine for Shan-D
Created by: ◉Ɗєиνιℓ 😎
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class AdvancedEmotionEngine:
    """Advanced emotion analysis and response system"""
    
    def __init__(self):
        self.emotion_patterns = {}
        logger.info("💝 AdvancedEmotionEngine initialized by ◉Ɗєиνιℓ 😏")
    
    async def analyze_emotion_ultra(
        self, 
        message: str, 
        conversation_history: List[Dict],
        user_profile: Dict
    ) -> Dict:
        """Ultra-advanced emotion analysis"""
        
        # Simplified emotion analysis
        emotion_analysis = {
            "primary_emotion": "neutral",
            "intensity": 0.5,
            "confidence": 0.8,
            "secondary_emotions": [],
            "context_emotion": "casual"
        }
        
        # Basic emotion detection
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["happy", "great", "awesome", "wonderful"]):
            emotion_analysis["primary_emotion"] = "happy"
            emotion_analysis["intensity"] = 0.8
        elif any(word in message_lower for word in ["sad", "upset", "disappointed"]):
            emotion_analysis["primary_emotion"] = "sad"
            emotion_analysis["intensity"] = 0.7
        elif any(word in message_lower for word in ["angry", "frustrated", "annoyed"]):
            emotion_analysis["primary_emotion"] = "angry"
            emotion_analysis["intensity"] = 0.7
        elif any(word in message_lower for word in ["excited", "thrilled", "amazing"]):
            emotion_analysis["primary_emotion"] = "excited"
            emotion_analysis["intensity"] = 0.9
        
        return emotion_analysis

"""
Shan-D Emotion Recognition and Response Engine
Advanced emotional intelligence with sentiment analysis and empathetic responses
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime, timedelta

class EmotionType(Enum):
    JOY = "joy"
    SADNESS = "sadness" 
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"
    EXCITEMENT = "excitement"
    FRUSTRATION = "frustration"
    ANXIETY = "anxiety"
    CONTENTMENT = "contentment"

class EmotionIntensity(Enum):
    VERY_LOW = 0.1
    LOW = 0.3
    MODERATE = 0.5
    HIGH = 0.7
    VERY_HIGH = 0.9

@dataclass
class EmotionAnalysis:
    primary_emotion: EmotionType
    intensity: float
    confidence: float
    secondary_emotions: List[Tuple[EmotionType, float]]
    emotional_context: Dict[str, Any]
    timestamp: datetime

class ShanDEmotionEngine:
    def __init__(self):
        self.emotion_patterns = self._load_emotion_patterns()
        self.user_emotion_history: Dict[str, List[EmotionAnalysis]] = {}
        self.empathetic_responses = self._load_empathetic_responses()
        
    def _load_emotion_patterns(self) -> Dict[EmotionType, List[str]]:
        """Load emotion detection patterns"""
        return {
            EmotionType.JOY: [
                r'\b(happy|joy|excited|amazing|wonderful|great|awesome|fantastic|love|pleased)\b',
                r'[😊😃😄😁🥳🎉✨💫⭐]',
                r'\b(yay|woohoo|hurray|celebrate)\b'
            ],
            EmotionType.SADNESS: [
                r'\b(sad|depressed|down|blue|upset|crying|tears|heartbroken|lonely|miserable)\b',
                r'[😢😭😞☹️💔😟]',
                r'\b(feel bad|feeling down|not good|terrible)\b'
            ],
            EmotionType.ANGER: [
                r'\b(angry|mad|furious|rage|pissed|annoyed|irritated|frustrated)\b',
                r'[😠😡🤬💢]',
                r'\b(hate|stupid|damn|wtf|annoying)\b'
            ],
            EmotionType.FEAR: [
                r'\b(scared|afraid|fear|terrified|worried|anxious|nervous|panic)\b',
                r'[😨😰😱]',
                r'\b(frightened|concerned|stress|overwhelmed)\b'
            ],
            EmotionType.SURPRISE: [
                r'\b(surprised|shocked|amazed|wow|incredible|unbelievable)\b',
                r'[😲😮🤯]',
                r'\b(oh my|no way|really|seriously)\b'
            ],
            EmotionType.EXCITEMENT: [
                r'\b(excited|thrilled|pumped|hyped|energized|enthusiastic)\b',
                r'[🤩🚀🔥⚡]',
                r'\b(can\'t wait|so ready|amazing opportunity)\b'
            ],
            EmotionType.FRUSTRATION: [
                r'\b(frustrated|stuck|annoying|difficult|complicated|confusing)\b',
                r'[😤🙄]',
                r'\b(why won\'t|doesn\'t work|so hard)\b'
            ],
            EmotionType.ANXIETY: [
                r'\b(anxious|worried|stress|nervous|overwhelmed|panic|concern)\b',
                r'[😰😟]',
                r'\b(what if|so worried|can\'t stop thinking)\b'
            ]
        }
    
    def _load_empathetic_responses(self) -> Dict[EmotionType, List[str]]:
        """Load empathetic response templates"""
        return {
            EmotionType.JOY: [
                "I'm so happy to hear that! Your joy is contagious! 🌟",
                "That's absolutely wonderful! I love sharing in your happiness! ✨",
                "Your excitement makes my day brighter! Tell me more! 😊"
            ],
            EmotionType.SADNESS: [
                "I can sense you're going through a tough time. I'm here for you 💙",
                "It's okay to feel sad. Your emotions are valid, and I'm here to support you 🤗",
                "I wish I could give you a hug right now. Let's work through this together 💪"
            ],
            EmotionType.ANGER: [
                "I can feel your frustration. Let's take a deep breath and work through this 🌸",
                "Your anger is understandable. Sometimes we need to let these feelings out 🌈",
                "I'm here to listen without judgment. What's really bothering you? 💭"
            ],
            EmotionType.FEAR: [
                "I understand you're feeling scared. Fear is natural, and you're brave for facing it 🛡️",
                "It's okay to feel afraid. Let's break this down into manageable pieces 🌱",
                "You're not alone in this. We'll tackle your fears one step at a time 🌟"
            ],
            EmotionType.EXCITEMENT: [
                "Your enthusiasm is infectious! I'm excited right along with you! 🚀",
                "This energy is amazing! Let's channel this excitement into something great! ⚡",
                "I love your passion! Tell me what's got you so pumped up! 🔥"
            ],
            EmotionType.FRUSTRATION: [
                "I can feel your frustration. These challenges can be really tough 🌿",
                "It's totally normal to feel stuck sometimes. Let's find a way through this 🗝️",
                "Your persistence is admirable. Let's tackle this problem together 🎯"
            ],
            EmotionType.ANXIETY: [
                "I sense your anxiety, and I want you to know it's completely normal 🌸",
                "Anxiety can be overwhelming. Let's take this one moment at a time 🧘‍♀️",
                "You're stronger than your worries. I'm here to help you through this 💝"
            ]
        }
    
    async def analyze_emotion(self, user_id: str, message: str, context: Dict[str, Any] = None) -> EmotionAnalysis:
        """Analyze emotional content of user message"""
        emotion_scores = {}
        
        # Pattern-based emotion detection
        for emotion_type, patterns in self.emotion_patterns.items():
            score = 0.0
            for pattern in patterns:
                matches = len(re.findall(pattern, message.lower()))
                score += matches * 0.3
            emotion_scores[emotion_type] = min(score, 1.0)
        
        # Contextual emotion analysis
        if context:
            emotion_scores = self._apply_contextual_analysis(emotion_scores, context)
        
        # Determine primary emotion
        if not emotion_scores or max(emotion_scores.values()) < 0.1:
            primary_emotion = EmotionType.NEUTRAL
            intensity = 0.1
            confidence = 0.5
        else:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            intensity = emotion_scores[primary_emotion]
            confidence = self._calculate_confidence(emotion_scores)
        
        # Find secondary emotions
        secondary_emotions = [
            (emotion, score) for emotion, score in emotion_scores.items() 
            if emotion != primary_emotion and score > 0.2
        ]
        secondary_emotions.sort(key=lambda x: x[1], reverse=True)
        secondary_emotions = secondary_emotions[:2]  # Top 2 secondary emotions
        
        analysis = EmotionAnalysis(
            primary_emotion=primary_emotion,
            intensity=intensity,
            confidence=confidence,
            secondary_emotions=secondary_emotions,
            emotional_context=context or {},
            timestamp=datetime.now()
        )
        
        # Store in emotion history
        if user_id not in self.user_emotion_history:
            self.user_emotion_history[user_id] = []
        self.user_emotion_history[user_id].append(analysis)
        
        # Keep only last 50 emotional states per user
        if len(self.user_emotion_history[user_id]) > 50:
            self.user_emotion_history[user_id] = self.user_emotion_history[user_id][-50:]
        
        return analysis
    
    def _apply_contextual_analysis(self, emotion_scores: Dict[EmotionType, float], context: Dict[str, Any]) -> Dict[EmotionType, float]:
        """Apply contextual information to emotion analysis"""
        # Time-based adjustments
        current_hour = datetime.now().hour
        if 22 <= current_hour or current_hour <= 6:  # Late night/early morning
            emotion_scores[EmotionType.ANXIETY] *= 1.2
            emotion_scores[EmotionType.SADNESS] *= 1.1
        
        # Message length considerations
        message_length = context.get('message_length', 0)
        if message_length > 500:  # Long messages might indicate strong emotions
            for emotion in emotion_scores:
                if emotion != EmotionType.NEUTRAL:
                    emotion_scores[emotion] *= 1.1
        
        # Previous emotion influence
        if 'previous_emotion' in context:
            prev_emotion = context['previous_emotion']
            if prev_emotion in emotion_scores:
                emotion_scores[prev_emotion] *= 1.15  # Emotional persistence
        
        return emotion_scores
    
    def _calculate_confidence(self, emotion_scores: Dict[EmotionType, float]) -> float:
        """Calculate confidence in emotion detection"""
        if not emotion_scores:
            return 0.0
        
        max_score = max(emotion_scores.values())
        sorted_scores = sorted(emotion_scores.values(), reverse=True)
        
        if len(sorted_scores) < 2:
            return max_score
        
        # Confidence based on difference between top two emotions
        confidence = max_score - sorted_scores[1]
        return min(max(confidence, 0.1), 1.0)
    
    def get_emotional_response(self, emotion_analysis: EmotionAnalysis) -> str:
        """Generate empathetic response based on emotion analysis"""
        emotion_type = emotion_analysis.primary_emotion
        
        if emotion_type in self.empathetic_responses:
            responses = self.empathetic_responses[emotion_type]
            # Weight responses by intensity
            if emotion_analysis.intensity > 0.7:
                # Use more intensive responses for high intensity emotions
                return responses[0] if responses else "I understand how you're feeling."
            else:
                return responses[min(1, len(responses)-1)] if len(responses) > 1 else responses[0]
        
        return "I hear you, and I'm here to help in any way I can. 💙"
    
    def get_emotion_trend(self, user_id: str, hours: int = 24) -> Dict[str, Any]:
        """Analyze emotional trends for a user over time"""
        if user_id not in self.user_emotion_history:
            return {'trend': 'neutral', 'dominant_emotions': []}
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_emotions = [
            analysis for analysis in self.user_emotion_history[user_id]
            if analysis.timestamp >= cutoff_time
        ]
        
        if not recent_emotions:
            return {'trend': 'neutral', 'dominant_emotions': []}
        
        # Calculate emotion frequencies
        emotion_counts = {}
        total_intensity = 0.0
        
        for analysis in recent_emotions:
            emotion = analysis.primary_emotion
            if emotion not in emotion_counts:
                emotion_counts[emotion] = {'count': 0, 'total_intensity': 0.0}
            
            emotion_counts[emotion]['count'] += 1
            emotion_counts[emotion]['total_intensity'] += analysis.intensity
            total_intensity += analysis.intensity
        
        # Determine dominant emotions
        dominant_emotions = []
        for emotion, data in emotion_counts.items():
            avg_intensity = data['total_intensity'] / data['count']
            dominant_emotions.append({
                'emotion': emotion.value,
                'frequency': data['count'] / len(recent_emotions),
                'average_intensity': avg_intensity
            })
        
        dominant_emotions.sort(key=lambda x: x['frequency'] * x['average_intensity'], reverse=True)
        
        # Determine overall trend
        avg_intensity = total_intensity / len(recent_emotions)
        if avg_intensity > 0.6:
            trend = 'intense'
        elif avg_intensity > 0.3:
            trend = 'moderate'
        else:
            trend = 'calm'
        
        return {
            'trend': trend,
            'dominant_emotions': dominant_emotions[:3],
            'analysis_period': f"{hours} hours",
            'total_interactions': len(recent_emotions)
        }
    
    def suggest_emotional_support(self, user_id: str) -> List[str]:
        """Suggest emotional support strategies based on user's emotional state"""
        if user_id not in self.user_emotion_history:
            return ["I'm here whenever you need someone to talk to! 💙"]
        
        recent_analysis = self.user_emotion_history[user_id][-1]
        emotion = recent_analysis.primary_emotion
        intensity = recent_analysis.intensity
        
        suggestions = []
        
        if emotion == EmotionType.SADNESS and intensity > 0.5:
            suggestions = [
                "Would you like to talk about what's making you feel this way?",
                "Sometimes it helps to express your feelings. I'm here to listen.",
                "Remember that it's okay to not be okay. You're not alone in this."
            ]
        elif emotion == EmotionType.ANXIETY and intensity > 0.5:
            suggestions = [
                "Let's try some breathing exercises together. Take a deep breath with me.",
                "What specific things are worrying you? We can tackle them one by one.",
                "Remember: you've overcome challenges before, and you can do it again."
            ]
        elif emotion == EmotionType.ANGER and intensity > 0.5:
            suggestions = [
                "It sounds like something really upset you. Want to tell me about it?",
                "Sometimes anger is a sign that something important to us is being threatened.",
                "Let's find a constructive way to address what's bothering you."
            ]
        elif emotion == EmotionType.JOY:
            suggestions = [
                "I love seeing you happy! What's bringing you so much joy?",
                "Your happiness is contagious! Tell me more about this positive experience.",
                "It's wonderful to celebrate the good moments with you!"
            ]
        else:
            suggestions = [
                "How are you feeling right now? I'm here to listen.",
                "Is there anything specific I can help you with today?",
                "I'm here to support you in whatever way you need."
            ]
        
        return suggestions
