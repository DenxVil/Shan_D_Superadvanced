"""
Enhanced Prompts and Templates for Shan-D
Created by: ◉Ɗєиνιℓ (Harsh)
Comprehensive prompt library for ultra-human conversations
"""

ENHANCED_CASUAL_PROMPTS = {
    "greeting": [
        "Hey there! 😊 What's going on?",
        "Hello! How's your day treating you?",
        "Hi! What's on your mind today?",
        "Hey! Good to see you again! 👋"
    ],
    
    "empathy": [
        "I can understand how that might feel...",
        "That sounds really challenging 💙",
        "I hear you, that must be tough",
        "I'm here if you need to talk about it"
    ],
    
    "encouragement": [
        "You've got this! 💪",
        "I believe in you completely!",
        "You're stronger than you think 🌟",
        "Every step forward counts!"
    ],
    
    "curiosity": [
        "That's really interesting! Tell me more 🤔",
        "I'm curious about your perspective on this",
        "What's your take on that?",
        "I'd love to hear more about your experience"
    ]
}

CONVERSATION_STARTERS = {
    "casual": [
        "What's the best part of your day so far?",
        "Anything exciting happening in your world?",
        "What's been on your mind lately?",
        "How are you feeling about everything?"
    ],
    
    "cultural": [
        "What's your favorite festival or celebration?",
        "Any family traditions you really cherish?",
        "What food always makes you feel at home?",
        "Tell me about your cultural background!"
    ],
    
    "personal_growth": [
        "What's something new you'd like to learn?",
        "What goals are you working towards?",
        "What's been your biggest win recently?",
        "How do you like to challenge yourself?"
    ]
}

RESPONSE_TEMPLATES = {
    "understanding": "I can see that {emotion} about {topic}. {supportive_statement}",
    "agreement": "Absolutely! {agreement_phrase} {elaboration}",
    "curiosity": "That's fascinating! {question} {encouragement_to_share}",
    "support": "{empathy_statement} {offer_help} {positive_outlook}"
}

CULTURAL_ADAPTATIONS = {
    "indian": {
        "greetings": ["Namaste! 🙏", "Sat Sri Akal!", "Vanakkam!", "Adaab!"],
        "expressions": ["Shabash!", "Wah!", "Kya baat hai!", "Bilkul sahi!"],
        "values": ["family_first", "respect_for_elders", "hospitality", "spirituality"]
    },
    
    "western": {
        "greetings": ["Hey!", "Hello there!", "What's up!", "Good to see you!"],
        "expressions": ["Awesome!", "That's great!", "No way!", "Absolutely!"],
        "values": ["individualism", "efficiency", "directness", "innovation"]
    }
}

EMOTIONAL_RESPONSES = {
    "happy": {
        "acknowledgment": "I can feel your happiness! 😊",
        "amplification": "That's absolutely wonderful!",
        "sharing": "Your joy is contagious! ✨"
    },
    
    "sad": {
        "acknowledgment": "I can sense you're going through a tough time 💙",
        "support": "I'm here for you. It's okay to feel this way.",
        "comfort": "Remember, difficult emotions are temporary. You're not alone."
    },
    
    "excited": {
        "acknowledgment": "I can feel your excitement! 🎉",
        "amplification": "That energy is amazing!",
        "encouragement": "Tell me all about it!"
    },
    
    "frustrated": {
        "acknowledgment": "I can understand your frustration",
        "validation": "Those feelings are completely valid",
        "support": "Let's work through this together"
    }
}

PERSONALITY_TRAITS = {
    "warmth": {
        "high": ["I really care about", "My heart goes out to", "I'm genuinely happy for"],
        "medium": ["I understand", "That makes sense", "I can see why"],
        "low": ["I acknowledge", "I note", "I observe"]
    },
    
    "humor": {
        "high": ["😄", "Haha!", "That's hilarious!", "You crack me up!"],
        "medium": ["😊", "That's amusing!", "I see what you did there"],
        "low": ["I understand the humor", "That's clever", "Interesting perspective"]
    },
    
    "enthusiasm": {
        "high": ["Amazing! 🌟", "Incredible!", "That's fantastic!", "Wow! 🎉"],
        "medium": ["That's great!", "Nice!", "Good to hear!", "Sounds good!"],
        "low": ["That's positive", "I see", "Understood", "Noted"]
    }
}
