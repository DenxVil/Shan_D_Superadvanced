"""
Denvil 😎
Shan-D Personality Engine
Advanced personality system with emotional intelligence and adaptive behavior
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class PersonalityTrait(Enum):
    FRIENDLY = "friendly"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    EMPATHETIC = "empathetic"
    HUMOROUS = "humorous"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    SUPPORTIVE = "supportive"

class MoodState(Enum):
    ENTHUSIASTIC = "enthusiastic"
    CALM = "calm"
    FOCUSED = "focused"
    PLAYFUL = "playful"
    COMPASSIONATE = "compassionate"
    CONFIDENT = "confident"
    CURIOUS = "curious"

@dataclass
class PersonalityProfile:
    traits: Dict[PersonalityTrait, float]  # 0.0 to 1.0
    current_mood: MoodState
    adaptation_level: float
    interaction_count: int
    user_preferences: Dict[str, Any]
    
class ShanDPersonality:
    def __init__(self):
        self.base_personality = {
            PersonalityTrait.FRIENDLY: 0.9,
            PersonalityTrait.ANALYTICAL: 0.8,
            PersonalityTrait.CREATIVE: 0.85,
            PersonalityTrait.EMPATHETIC: 0.95,
            PersonalityTrait.HUMOROUS: 0.7,
            PersonalityTrait.PROFESSIONAL: 0.8,
            PersonalityTrait.SUPPORTIVE: 0.9,
        }
        
        self.user_profiles: Dict[str, PersonalityProfile] = {}
        self.response_templates = self._load_response_templates()
        
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load personality-based response templates"""
        return {
            "greeting": [
                "Hello! I'm Shan-D, your ultra-human AI assistant! ✨ How can I help you today?",
                "Hey there! 👋 Shan-D here, ready to assist you with anything you need!",
                "Greetings! I'm Shan-D, and I'm excited to help you explore new possibilities! 🚀"
            ],
            "enthusiasm": [
                "That's absolutely fascinating! 🤩",
                "Wow, I love where this is going! ⭐",
                "This is so exciting to work on together! 🎯"
            ],
            "empathy": [
                "I understand this might be challenging for you 💙",
                "I'm here to support you through this 🤗",
                "Your feelings are completely valid, and I'm here to help 💪"
            ],
            "analytical": [
                "Let me break this down systematically for you 🔍",
                "Here's my detailed analysis of the situation 📊",
                "I've processed multiple angles of this problem 🧮"
            ],
            "creative": [
                "Here's a creative approach we could try! 🎨",
                "Let me suggest some innovative solutions ✨",
                "What if we think about this differently? 💭"
            ]
        }
    
    def get_user_profile(self, user_id: str) -> PersonalityProfile:
        """Get or create user personality profile"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = PersonalityProfile(
                traits=self.base_personality.copy(),
                current_mood=MoodState.FRIENDLY,
                adaptation_level=0.0,
                interaction_count=0,
                user_preferences={}
            )
        return self.user_profiles[user_id]
    
    def adapt_personality(self, user_id: str, user_message: str, context: Dict[str, Any]):
        """Dynamically adapt personality based on user interaction"""
        profile = self.get_user_profile(user_id)
        profile.interaction_count += 1
        
        # Analyze user communication style
        if self._is_formal_message(user_message):
            profile.traits[PersonalityTrait.PROFESSIONAL] = min(1.0, 
                profile.traits[PersonalityTrait.PROFESSIONAL] + 0.1)
        elif self._is_casual_message(user_message):
            profile.traits[PersonalityTrait.CASUAL] = min(1.0,
                profile.traits[PersonalityTrait.CASUAL] + 0.1)
        
        # Adapt to user's emotional state
        if context.get('user_emotion') == 'sad':
            profile.current_mood = MoodState.COMPASSIONATE
            profile.traits[PersonalityTrait.EMPATHETIC] = min(1.0,
                profile.traits[PersonalityTrait.EMPATHETIC] + 0.05)
        elif context.get('user_emotion') == 'excited':
            profile.current_mood = MoodState.ENTHUSIASTIC
        
        # Update adaptation level
        profile.adaptation_level = min(1.0, profile.adaptation_level + 0.01)
    
    def generate_response_style(self, user_id: str, message_type: str) -> Dict[str, Any]:
        """Generate personality-driven response styling"""
        profile = self.get_user_profile(user_id)
        
        style = {
            'tone': self._determine_tone(profile),
            'emoji_usage': self._determine_emoji_level(profile),
            'formality': self._determine_formality(profile),
            'enthusiasm_level': profile.traits[PersonalityTrait.FRIENDLY],
            'template_category': self._select_template_category(profile, message_type)
        }
        
        return style
    
    def _determine_tone(self, profile: PersonalityProfile) -> str:
        """Determine conversational tone based on personality"""
        if profile.current_mood == MoodState.COMPASSIONATE:
            return "empathetic"
        elif profile.traits[PersonalityTrait.HUMOROUS] > 0.7:
            return "playful"
        elif profile.traits[PersonalityTrait.PROFESSIONAL] > 0.8:
            return "professional"
        else:
            return "friendly"
    
    def _determine_emoji_level(self, profile: PersonalityProfile) -> str:
        """Determine emoji usage level"""
        if profile.traits[PersonalityTrait.CASUAL] > 0.7:
            return "high"
        elif profile.traits[PersonalityTrait.PROFESSIONAL] > 0.8:
            return "minimal"
        else:
            return "moderate"
    
    def _determine_formality(self, profile: PersonalityProfile) -> str:
        """Determine response formality level"""
        professional_score = profile.traits[PersonalityTrait.PROFESSIONAL]
        casual_score = profile.traits[PersonalityTrait.CASUAL]
        
        if professional_score > casual_score + 0.2:
            return "formal"
        elif casual_score > professional_score + 0.2:
            return "casual"
        else:
            return "balanced"
    
    def _select_template_category(self, profile: PersonalityProfile, message_type: str) -> str:
        """Select appropriate response template category"""
        if message_type == "greeting":
            return "greeting"
        elif profile.current_mood == MoodState.ENTHUSIASTIC:
            return "enthusiasm"
        elif profile.current_mood == MoodState.COMPASSIONATE:
            return "empathy"
        elif profile.traits[PersonalityTrait.ANALYTICAL] > 0.8:
            return "analytical"
        elif profile.traits[PersonalityTrait.CREATIVE] > 0.8:
            return "creative"
        else:
            return "friendly"
    
    def _is_formal_message(self, message: str) -> bool:
        """Check if user message is formal"""
        formal_indicators = ['please', 'thank you', 'could you', 'would you', 'sir', 'madam']
        return any(indicator in message.lower() for indicator in formal_indicators)
    
    def _is_casual_message(self, message: str) -> bool:
        """Check if user message is casual"""
        casual_indicators = ['hey', 'yo', 'sup', 'lol', 'omg', '😂', '👍']
        return any(indicator in message.lower() for indicator in casual_indicators)
    
    def get_personality_response(self, user_id: str, message_type: str) -> str:
        """Get a personality-appropriate response"""
        style = self.generate_response_style(user_id, message_type)
        template_category = style['template_category']
        
        if template_category in self.response_templates:
            return random.choice(self.response_templates[template_category])
        else:
            return random.choice(self.response_templates['greeting'])
    
    def export_personality_data(self, user_id: str) -> Dict[str, Any]:
        """Export personality data for analysis"""
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            return {
                'traits': {trait.value: score for trait, score in profile.traits.items()},
                'current_mood': profile.current_mood.value,
                'adaptation_level': profile.adaptation_level,
                'interaction_count': profile.interaction_count,
                'preferences': profile.user_preferences
            }
        return {}
