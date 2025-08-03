#Denvil
"""
Shan-D Enhanced Conversation Flow Manager
Manages natural conversation flow, context switching, dialogue coherence, and advanced user profiling
Version: 4.0 Ultra-Enhanced
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime, timedelta
import json
import logging
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationState(Enum):
    """Enhanced conversation states with more granular control"""
    GREETING = "greeting"
    ACTIVE = "active"
    QUESTION_ANSWERING = "question_answering"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVE_COLLABORATION = "creative_collaboration"
    EMOTIONAL_SUPPORT = "emotional_support"
    LEARNING_SESSION = "learning_session"
    TECHNICAL_DISCUSSION = "technical_discussion"
    CASUAL_CHAT = "casual_chat"
    DEEP_ANALYSIS = "deep_analysis"
    WRAPPING_UP = "wrapping_up"
    IDLE = "idle"
    EMERGENCY_SUPPORT = "emergency_support"

class FlowTransition(Enum):
    """Flow transition types"""
    CONTINUE = "continue"
    ESCALATE = "escalate"
    PIVOT = "pivot"
    CONCLUDE = "conclude"
    RESET = "reset"
    EMERGENCY = "emergency"

class PersonalityMode(Enum):
    """User personality adaptation modes"""
    ANALYTICAL = "analytical"
    CREATIVE = "creative" 
    SUPPORTIVE = "supportive"
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"

@dataclass
class ConversationMetrics:
    """Track detailed conversation metrics"""
    total_messages: int = 0
    average_response_time: float = 0.0
    engagement_score: float = 0.5
    complexity_level: float = 0.5
    emotional_intensity: float = 0.0
    topic_diversity: int = 0
    learning_progress: float = 0.0

@dataclass
class ConversationFlow:
    """Enhanced conversation flow with comprehensive tracking"""
    user_id: str
    current_state: ConversationState
    previous_state: ConversationState
    context_depth: int = 0
    topic_thread: List[str] = field(default_factory=list)
    engagement_level: float = 0.5
    flow_momentum: float = 0.0
    last_transition: datetime = field(default_factory=datetime.now)
    pending_topics: List[str] = field(default_factory=list)
    personality_mode: PersonalityMode = PersonalityMode.CASUAL
    metrics: ConversationMetrics = field(default_factory=ConversationMetrics)
    conversation_history: deque = field(default_factory=lambda: deque(maxlen=50))
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    emotional_state_history: List[Dict[str, Any]] = field(default_factory=list)
    learning_topics: Set[str] = field(default_factory=set)

class ShanDConversationFlow:
    """Enhanced Shan-D Conversation Flow Manager with advanced features"""
    
    def __init__(self):
        self.user_flows: Dict[str, ConversationFlow] = {}
        self.state_transitions = self._init_state_transitions()
        self.engagement_indicators = self._init_engagement_indicators()
        self.personality_adapters = self._init_personality_adapters()
        self.emergency_keywords = self._init_emergency_keywords()
        self.learning_patterns = defaultdict(list)
        
    def _init_state_transitions(self) -> Dict[ConversationState, List[ConversationState]]:
        """Initialize comprehensive state transitions"""
        return {
            ConversationState.GREETING: [
                ConversationState.ACTIVE,
                ConversationState.QUESTION_ANSWERING,
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.CASUAL_CHAT,
                ConversationState.EMERGENCY_SUPPORT
            ],
            ConversationState.ACTIVE: [
                ConversationState.QUESTION_ANSWERING,
                ConversationState.PROBLEM_SOLVING,
                ConversationState.CREATIVE_COLLABORATION,
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.LEARNING_SESSION,
                ConversationState.TECHNICAL_DISCUSSION,
                ConversationState.CASUAL_CHAT,
                ConversationState.DEEP_ANALYSIS,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.QUESTION_ANSWERING: [
                ConversationState.ACTIVE,
                ConversationState.PROBLEM_SOLVING,
                ConversationState.LEARNING_SESSION,
                ConversationState.DEEP_ANALYSIS,
                ConversationState.TECHNICAL_DISCUSSION,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.PROBLEM_SOLVING: [
                ConversationState.ACTIVE,
                ConversationState.CREATIVE_COLLABORATION,
                ConversationState.LEARNING_SESSION,
                ConversationState.TECHNICAL_DISCUSSION,
                ConversationState.DEEP_ANALYSIS,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.CREATIVE_COLLABORATION: [
                ConversationState.ACTIVE,
                ConversationState.PROBLEM_SOLVING,
                ConversationState.CASUAL_CHAT,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.EMOTIONAL_SUPPORT: [
                ConversationState.ACTIVE,
                ConversationState.CASUAL_CHAT,
                ConversationState.WRAPPING_UP,
                ConversationState.EMERGENCY_SUPPORT,
                ConversationState.IDLE
            ],
            ConversationState.LEARNING_SESSION: [
                ConversationState.ACTIVE,
                ConversationState.QUESTION_ANSWERING,
                ConversationState.TECHNICAL_DISCUSSION,
                ConversationState.DEEP_ANALYSIS,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.TECHNICAL_DISCUSSION: [
                ConversationState.ACTIVE,
                ConversationState.PROBLEM_SOLVING,
                ConversationState.LEARNING_SESSION,
                ConversationState.DEEP_ANALYSIS,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.CASUAL_CHAT: [
                ConversationState.ACTIVE,
                ConversationState.CREATIVE_COLLABORATION,
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.DEEP_ANALYSIS: [
                ConversationState.ACTIVE,
                ConversationState.TECHNICAL_DISCUSSION,
                ConversationState.LEARNING_SESSION,
                ConversationState.PROBLEM_SOLVING,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.WRAPPING_UP: [
                ConversationState.IDLE,
                ConversationState.ACTIVE,
                ConversationState.CASUAL_CHAT
            ],
            ConversationState.IDLE: [
                ConversationState.GREETING,
                ConversationState.ACTIVE,
                ConversationState.CASUAL_CHAT
            ],
            ConversationState.EMERGENCY_SUPPORT: [
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.IDLE,
                ConversationState.WRAPPING_UP
            ]
        }
    
    def _init_engagement_indicators(self) -> Dict[str, Dict[str, float]]:
        """Initialize enhanced engagement level indicators"""
        return {
            'high_engagement': {
                'multiple_questions': 0.8,
                'detailed_responses': 0.7,
                'follow_up_questions': 0.9,
                'personal_sharing': 0.8,
                'enthusiasm_markers': 0.6,
                'technical_depth': 0.7,
                'creative_input': 0.8,
                'emotional_openness': 0.9
            },
            'medium_engagement': {
                'single_questions': 0.5,
                'brief_responses': 0.4,
                'acknowledgments': 0.3,
                'topic_continuation': 0.5,
                'clarification_requests': 0.6,
                'moderate_detail': 0.5
            },
            'low_engagement': {
                'short_answers': 0.2,
                'topic_changes': 0.1,
                'delayed_responses': 0.1,
                'generic_responses': 0.2,
                'minimal_interaction': 0.1,
                'disengagement_signals': 0.0
            }
        }
    
    def _init_personality_adapters(self) -> Dict[PersonalityMode, Dict[str, Any]]:
        """Initialize personality adaptation settings"""
        return {
            PersonalityMode.ANALYTICAL: {
                'response_style': 'detailed_logical',
                'preferred_states': [ConversationState.DEEP_ANALYSIS, ConversationState.TECHNICAL_DISCUSSION],
                'engagement_boost': 0.8,
                'complexity_preference': 0.9
            },
            PersonalityMode.CREATIVE: {
                'response_style': 'imaginative_open',
                'preferred_states': [ConversationState.CREATIVE_COLLABORATION, ConversationState.CASUAL_CHAT],
                'engagement_boost': 0.7,
                'complexity_preference': 0.6
            },
            PersonalityMode.SUPPORTIVE: {
                'response_style': 'empathetic_caring',
                'preferred_states': [ConversationState.EMOTIONAL_SUPPORT, ConversationState.LEARNING_SESSION],
                'engagement_boost': 0.9,
                'complexity_preference': 0.4
            },
            PersonalityMode.CASUAL: {
                'response_style': 'friendly_relaxed',
                'preferred_states': [ConversationState.CASUAL_CHAT, ConversationState.ACTIVE],
                'engagement_boost': 0.6,
                'complexity_preference': 0.5
            },
            PersonalityMode.PROFESSIONAL: {
                'response_style': 'formal_structured',
                'preferred_states': [ConversationState.TECHNICAL_DISCUSSION, ConversationState.PROBLEM_SOLVING],
                'engagement_boost': 0.7,
                'complexity_preference': 0.8
            },
            PersonalityMode.HUMOROUS: {
                'response_style': 'witty_playful',
                'preferred_states': [ConversationState.CASUAL_CHAT, ConversationState.CREATIVE_COLLABORATION],
                'engagement_boost': 0.8,
                'complexity_preference': 0.3
            }
        }
    
    def _init_emergency_keywords(self) -> List[str]:
        """Initialize emergency detection keywords"""
        return [
            'suicide', 'kill myself', 'end it all', 'can\'t go on', 
            'hopeless', 'worthless', 'emergency', 'crisis', 'help me',
            'in danger', 'hurt myself', 'self harm', 'desperate'
        ]
    
    def get_user_flow(self, user_id: str) -> ConversationFlow:
        """Get or create enhanced conversation flow for user"""
        if user_id not in self.user_flows:
            self.user_flows[user_id] = ConversationFlow(
                user_id=user_id,
                current_state=ConversationState.GREETING,
                previous_state=ConversationState.IDLE,
                context_depth=0,
                topic_thread=[],
                engagement_level=0.5,
                flow_momentum=0.0,
                last_transition=datetime.now(),
                pending_topics=[],
                personality_mode=PersonalityMode.CASUAL,
                metrics=ConversationMetrics(),
                conversation_history=deque(maxlen=50),
                user_preferences={},
                emotional_state_history=[],
                learning_topics=set()
            )
        return self.user_flows[user_id]
    
    async def process_message_flow(self, user_id: str, message: str,
                                 emotion_data: Dict[str, Any],
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Process message and update enhanced conversation flow"""
        flow = self.get_user_flow(user_id)
        
        # Record message in history
        flow.conversation_history.append({
            'timestamp': datetime.now(),
            'message': message,
            'emotion_data': emotion_data,
            'state': flow.current_state.value
        })
        
        # Check for emergency situations first
        if self._detect_emergency(message):
            flow.current_state = ConversationState.EMERGENCY_SUPPORT
            return self._handle_emergency_response(flow, message)
        
        # Analyze message characteristics
        message_analysis = self._analyze_message(message)
        
        # Update user personality mode based on patterns
        self._update_personality_mode(flow, message_analysis)
        
        # Update engagement level
        flow.engagement_level = self._calculate_engagement(
            flow.engagement_level,
            message_analysis,
            emotion_data
        )
        
        # Update conversation metrics
        self._update_metrics(flow, message_analysis, emotion_data)
        
        # Determine appropriate state transition
        new_state = await self._determine_state_transition(
            flow, message_analysis, emotion_data, context
        )
        
        # Update flow state if changed
        if new_state != flow.current_state:
            flow.previous_state = flow.current_state
            flow.current_state = new_state
            flow.last_transition = datetime.now()
            logger.info(f"State transition: {flow.previous_state.value} -> {new_state.value}")
        
        # Update context tracking
        self._update_context_tracking(flow, message_analysis)
        
        # Calculate flow momentum
        flow.flow_momentum = self._calculate_momentum(flow, message_analysis)
        
        # Generate comprehensive response strategy
        response_strategy = self._generate_response_strategy(flow, message_analysis)
        
        # Track learning progress
        self._update_learning_progress(flow, message_analysis)
        
        return {
            'current_state': flow.current_state.value,
            'previous_state': flow.previous_state.value,
            'engagement_level': round(flow.engagement_level, 3),
            'flow_momentum': round(flow.flow_momentum, 3),
            'context_depth': flow.context_depth,
            'personality_mode': flow.personality_mode.value,
            'response_strategy': response_strategy,
            'topic_thread': flow.topic_thread[-5:],  # Last 5 topics
            'pending_topics': flow.pending_topics,
            'metrics': {
                'total_messages': flow.metrics.total_messages,
                'engagement_score': round(flow.metrics.engagement_score, 3),
                'complexity_level': round(flow.metrics.complexity_level, 3),
                'emotional_intensity': round(flow.metrics.emotional_intensity, 3),
                'learning_progress': round(flow.metrics.learning_progress, 3)
            },
            'user_preferences': flow.user_preferences,
            'recommended_actions': self._get_recommended_actions(flow)
        }
    
    def _detect_emergency(self, message: str) -> bool:
        """Detect emergency situations requiring immediate support"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.emergency_keywords)
    
    def _handle_emergency_response(self, flow: ConversationFlow, message: str) -> Dict[str, Any]:
        """Handle emergency situations with immediate supportive response"""
        flow.engagement_level = 1.0
        flow.flow_momentum = 1.0
        
        return {
            'current_state': ConversationState.EMERGENCY_SUPPORT.value,
            'emergency_detected': True,
            'priority_response': True,
            'response_strategy': {
                'tone': 'urgent_supportive',
                'detail_level': 'immediate_care',
                'interaction_style': 'crisis_intervention',
                'emergency_resources': True,
                'professional_help_recommended': True
            }
        }
    
    def _analyze_message(self, message: str) -> Dict[str, Any]:
        """Enhanced message analysis with comprehensive features"""
        words = message.split()
        word_count = len(words)
        
        analysis = {
            'length': len(message),
            'word_count': word_count,
            'question_count': message.count('?'),
            'exclamation_count': message.count('!'),
            'has_code': '```',
            'has_personal_info': any(word in message.lower() for word in [
                'i am', 'my', 'me', 'personally', 'myself', 'i feel', 'i think'
            ]),
            'has_problem': any(word in message.lower() for word in [
                'problem', 'issue', 'help', 'stuck', 'error', 'bug', 'broken', 'wrong'
            ]),
            'has_creative_request': any(word in message.lower() for word in [
                'create', 'design', 'brainstorm', 'idea', 'imagine', 'invent', 'build'
            ]),
            'has_learning_intent': any(word in message.lower() for word in [
                'learn', 'teach', 'explain', 'understand', 'how', 'what', 'why', 'tutorial'
            ]),
            'has_emotional_content': any(word in message.lower() for word in [
                'feel', 'sad', 'happy', 'worried', 'excited', 'angry', 'frustrated', 'joy'
            ]),
            'has_technical_content': any(word in message.lower() for word in [
                'algorithm', 'function', 'variable', 'loop', 'api', 'database', 'server'
            ]),
            'has_casual_markers': any(word in message.lower() for word in [
                'lol', 'haha', 'awesome', 'cool', 'nice', 'great', 'amazing'
            ]),
            'has_formal_markers': any(word in message.lower() for word in [
                'please', 'thank you', 'respectfully', 'sincerely', 'regarding'
            ]),
            'complexity_score': self._calculate_complexity(message),
            'sentiment_indicators': self._analyze_sentiment(message),
            'urgency_level': self._calculate_urgency(message),
            'creativity_level': self._calculate_creativity(message)
        }
        
        return analysis
    
    def _calculate_complexity(self, message: str) -> float:
        """Calculate enhanced message complexity score"""
        words = message.split()
        if not words:
            return 0.0
        
        # Multiple complexity factors
        avg_word_length = sum(len(word) for word in words) / len(words)
        sentence_count = len([s for s in message.split('.') if s.strip()])
        technical_terms = len([word for word in words if len(word) > 8])
        punctuation_variety = len(set(char for char in message if char in '.,!?;:'))
        
        complexity = (
            (avg_word_length / 10) * 0.3 +
            (len(words) / 100) * 0.2 +
            (technical_terms / max(len(words), 1)) * 0.3 +
            (punctuation_variety / 6) * 0.2
        )
        
        return min(complexity, 1.0)
    
    def _analyze_sentiment(self, message: str) -> Dict[str, float]:
        """Basic sentiment analysis"""
        positive_words = ['good', 'great', 'awesome', 'excellent', 'happy', 'love', 'amazing']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 'frustrated']
        
        message_lower = message.lower()
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        total_words = len(message.split())
        if total_words == 0:
            return {'positive': 0.5, 'negative': 0.5, 'neutral': 0.5}
        
        positive_score = positive_count / total_words
        negative_score = negative_count / total_words
        neutral_score = 1.0 - (positive_score + negative_score)
        
        return {
            'positive': min(positive_score * 5, 1.0),
            'negative': min(negative_score * 5, 1.0),
            'neutral': max(neutral_score, 0.0)
        }
    
    def _calculate_urgency(self, message: str) -> float:
        """Calculate message urgency level"""
        urgent_markers = ['urgent', 'asap', 'immediately', 'now', 'quick', 'fast', 'emergency']
        exclamation_count = message.count('!')
        caps_ratio = sum(1 for c in message if c.isupper()) / max(len(message), 1)
        
        urgency = 0.0
        urgency += sum(0.2 for marker in urgent_markers if marker in message.lower())
        urgency += min(exclamation_count * 0.1, 0.3)
        urgency += min(caps_ratio * 0.5, 0.4)
        
        return min(urgency, 1.0)
    
    def _calculate_creativity(self, message: str) -> float:
        """Calculate creativity level in message"""
        creative_markers = ['imagine', 'creative', 'innovative', 'unique', 'original', 'artistic']
        metaphor_indicators = ['like', 'as if', 'similar to', 'reminds me of']
        
        creativity = 0.0
        creativity += sum(0.15 for marker in creative_markers if marker in message.lower())
        creativity += sum(0.1 for indicator in metaphor_indicators if indicator in message.lower())
        
        # Check for unusual word combinations or expressions
        words = message.split()
        if len(words) > 5:
            creativity += 0.1
        
        return min(creativity, 1.0)
    
    def _update_personality_mode(self, flow: ConversationFlow, message_analysis: Dict[str, Any]):
        """Update user personality mode based on interaction patterns"""
        # Analyze patterns over recent messages
        recent_messages = list(flow.conversation_history)[-10:]
        
        if len(recent_messages) < 3:
            return
        
        # Count characteristics
        technical_count = sum(1 for msg in recent_messages 
                            if 'technical' in str(msg.get('message', '')).lower())
        creative_count = sum(1 for msg in recent_messages 
                           if any(word in str(msg.get('message', '')).lower() 
                                for word in ['create', 'imagine', 'design']))
        emotional_count = sum(1 for msg in recent_messages 
                            if any(word in str(msg.get('message', '')).lower() 
                                 for word in ['feel', 'emotion', 'sad', 'happy']))
        
        # Update personality mode based on patterns
        if technical_count >= 3:
            flow.personality_mode = PersonalityMode.ANALYTICAL
        elif creative_count >= 3:
            flow.personality_mode = PersonalityMode.CREATIVE
        elif emotional_count >= 3:
            flow.personality_mode = PersonalityMode.SUPPORTIVE
        elif message_analysis['has_casual_markers']:
            flow.personality_mode = PersonalityMode.CASUAL
        elif message_analysis['has_formal_markers']:
            flow.personality_mode = PersonalityMode.PROFESSIONAL
    
    def _calculate_engagement(self, current_engagement: float,
                            message_analysis: Dict[str, Any],
                            emotion_data: Dict[str, Any]) -> float:
        """Calculate enhanced engagement level"""
        engagement_delta = 0.0
        
        # Message length and detail
        if message_analysis['word_count'] > 20:
            engagement_delta += 0.15
        elif message_analysis['word_count'] < 5:
            engagement_delta -= 0.1
        
        # Questions and interaction
        engagement_delta += message_analysis['question_count'] * 0.2
        engagement_delta += message_analysis['exclamation_count'] * 0.05
        
        # Content type bonuses
        if message_analysis['has_personal_info']:
            engagement_delta += 0.25
        if message_analysis['has_technical_content']:
            engagement_delta += 0.15
        if message_analysis['has_creative_request']:
            engagement_delta += 0.2
        
        # Complexity and depth
        engagement_delta += message_analysis['complexity_score'] * 0.15
        
        # Emotional intensity
        if emotion_data and 'intensity' in emotion_data:
            engagement_delta += emotion_data['intensity'] * 0.1
        
        # Sentiment impact
        sentiment = message_analysis.get('sentiment_indicators', {})
        if sentiment.get('positive', 0) > 0.5:
            engagement_delta += 0.1
        elif sentiment.get('negative', 0) > 0.5:
            engagement_delta += 0.05  # Negative emotions can also indicate engagement
        
        # Apply changes with smoothing
        new_engagement = current_engagement + (engagement_delta * 0.6)
        return max(0.0, min(1.0, new_engagement))
    
    def _update_metrics(self, flow: ConversationFlow, message_analysis: Dict[str, Any], 
                       emotion_data: Dict[str, Any]):
        """Update comprehensive conversation metrics"""
        metrics = flow.metrics
        
        # Update basic counters
        metrics.total_messages += 1
        
        # Update running averages
        alpha = 0.7  # Smoothing factor
        metrics.engagement_score = (alpha * flow.engagement_level + 
                                  (1 - alpha) * metrics.engagement_score)
        metrics.complexity_level = (alpha * message_analysis['complexity_score'] + 
                                  (1 - alpha) * metrics.complexity_level)
        
        # Update emotional intensity
        if emotion_data and 'intensity' in emotion_data:
            metrics.emotional_intensity = (alpha * emotion_data['intensity'] + 
                                         (1 - alpha) * metrics.emotional_intensity)
        
        # Update topic diversity
        current_topics = set(flow.topic_thread)
        metrics.topic_diversity = len(current_topics)
    
    async def _determine_state_transition(self, flow: ConversationFlow,
                                        message_analysis: Dict[str, Any],
                                        emotion_data: Dict[str, Any],
                                        context: Dict[str, Any]) -> ConversationState:
        """Determine appropriate state transition with enhanced logic"""
        current_state = flow.current_state
        
        # Emergency check (highest priority)
        if self._detect_emergency(context.get('message', '')):
            return ConversationState.EMERGENCY_SUPPORT
        
        # Strong emotional support needed
        if emotion_data.get('primary_emotion') in ['sadness', 'anger', 'fear', 'anxiety']:
            if emotion_data.get('intensity', 0) > 0.7:
                return ConversationState.EMOTIONAL_SUPPORT
        
        # High technical content
        if message_analysis['has_technical_content'] and message_analysis['complexity_score'] > 0.7:
            return ConversationState.TECHNICAL_DISCUSSION
        
        # Deep analysis request
        if (message_analysis['word_count'] > 50 and 
            message_analysis['complexity_score'] > 0.8):
            return ConversationState.DEEP_ANALYSIS
        
        # State-specific transitions
        if current_state == ConversationState.GREETING:
            if message_analysis['has_problem']:
                return ConversationState.PROBLEM_SOLVING
            elif message_analysis['has_learning_intent']:
                return ConversationState.LEARNING_SESSION
            elif message_analysis['has_creative_request']:
                return ConversationState.CREATIVE_COLLABORATION
            elif message_analysis['has_technical_content']:
                return ConversationState.TECHNICAL_DISCUSSION
            elif message_analysis['question_count'] > 0:
                return ConversationState.QUESTION_ANSWERING
            elif message_analysis['has_casual_markers']:
                return ConversationState.CASUAL_CHAT
            else:
                return ConversationState.ACTIVE
        
        elif current_state == ConversationState.ACTIVE:
            if message_analysis['has_problem']:
                return ConversationState.PROBLEM_SOLVING
            elif message_analysis['has_creative_request']:
                return ConversationState.CREATIVE_COLLABORATION
            elif message_analysis['has_learning_intent']:
                return ConversationState.LEARNING_SESSION
            elif message_analysis['has_technical_content']:
                return ConversationState.TECHNICAL_DISCUSSION
            elif message_analysis['question_count'] > 0:
                return ConversationState.QUESTION_ANSWERING
            elif message_analysis['has_casual_markers']:
                return ConversationState.CASUAL_CHAT
        
        # Check for conversation wrap-up signals
        wrap_up_signals = [
            'thanks', 'thank you', 'that\'s all', 'goodbye', 'bye', 
            'see you', 'talk later', 'gotta go', 'that\'s enough'
        ]
        message_lower = context.get('message', '').lower()
        if any(signal in message_lower for signal in wrap_up_signals):
            if current_state != ConversationState.WRAPPING_UP:
                return ConversationState.WRAPPING_UP
        
        # Check for momentum decline
        if (flow.flow_momentum < 0.2 and flow.engagement_level < 0.3):
            time_since_transition = datetime.now() - flow.last_transition
            if time_since_transition > timedelta(minutes=10):
                return ConversationState.WRAPPING_UP
        
        return current_state
    
    def _update_context_tracking(self, flow: ConversationFlow, message_analysis: Dict[str, Any]):
        """Enhanced context depth and topic tracking"""
        # Update context depth
        if (message_analysis['complexity_score'] > 0.6 or 
            message_analysis['word_count'] > 40):
            flow.context_depth = min(flow.context_depth + 1, 15)
        elif message_analysis['word_count'] < 10:
            flow.context_depth = max(flow.context_depth - 1, 0)
        
        # Extract and track topics
        potential_topics = []
        if message_analysis['has_problem']:
            potential_topics.append('problem_solving')
        if message_analysis['has_creative_request']:
            potential_topics.append('creativity')
        if message_analysis['has_learning_intent']:
            potential_topics.append('learning')
        if message_analysis['has_code']:
            potential_topics.append('programming')
        if message_analysis['has_technical_content']:
            potential_topics.append('technical')
        if message_analysis['has_emotional_content']:
            potential_topics.append('emotional')
        
        # Add new topics to thread
        for topic in potential_topics:
            if topic not in flow.topic_thread[-5:]:  # Avoid recent duplicates
                flow.topic_thread.append(topic)
                flow.learning_topics.add(topic)
        
        # Maintain manageable topic thread
        if len(flow.topic_thread) > 20:
            flow.topic_thread = flow.topic_thread[-20:]
    
    def _calculate_momentum(self, flow: ConversationFlow, message_analysis: Dict[str, Any]) -> float:
        """Calculate enhanced conversation flow momentum"""
        base_momentum = 0.4
        
        # Engagement boost
        momentum_boost = flow.engagement_level * 0.4
        
        # Context depth indicates sustained conversation
        context_boost = min(flow.context_depth / 15, 0.25)
        
        # Interaction richness
        interaction_boost = (
            message_analysis['question_count'] * 0.1 +
            message_analysis['exclamation_count'] * 0.05 +
            (1 if message_analysis['has_personal_info'] else 0) * 0.15
        )
        
        # Recent activity boost
        time_since_transition = datetime.now() - flow.last_transition
        if time_since_transition < timedelta(minutes=1):
            recency_boost = 0.3
        elif time_since_transition < timedelta(minutes=5):
            recency_boost = 0.15
        else:
            # Gradual decay over 15 minutes
            recency_boost = max(0, 0.15 - (time_since_transition.seconds / 900))
        
        # Personality mode influence
        personality_boost = self.personality_adapters[flow.personality_mode]['engagement_boost'] * 0.1
        
        total_momentum = (base_momentum + momentum_boost + context_boost + 
                         interaction_boost + recency_boost + personality_boost)
        
        return max(0.0, min(1.0, total_momentum))
    
    def _update_learning_progress(self, flow: ConversationFlow, message_analysis: Dict[str, Any]):
        """Track and update learning progress"""
        if message_analysis['has_learning_intent']:
            flow.metrics.learning_progress = min(flow.metrics.learning_progress + 0.05, 1.0)
        
        # Track learning patterns
        if flow.current_state == ConversationState.LEARNING_SESSION:
            learning_topic = flow.topic_thread[-1] if flow.topic_thread else 'general'
            self.learning_patterns[flow.user_id].append({
                'topic': learning_topic,
                'timestamp': datetime.now(),
                'complexity': message_analysis['complexity_score']
            })
    
    def _generate_response_strategy(self, flow: ConversationFlow,
                                  message_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive response strategy"""
        personality_config = self.personality_adapters[flow.personality_mode]
        
        base_strategy = {
            'tone': 'balanced',
            'detail_level': 'medium',
            'interaction_style': 'collaborative',
            'follow_up_suggestions': [],
            'transition_hints': [],
            'personality_mode': flow.personality_mode.value,
            'preferred_response_length': 'medium',
            'technical_level': 'moderate',
            'emotional_support_level': 'standard'
        }
        
        # Apply personality-based modifications
        base_strategy['interaction_style'] = personality_config['response_style']
        
        # State-specific strategies
        state_strategies = {
            ConversationState.GREETING: {
                'tone': 'welcoming',
                'interaction_style': 'friendly',
                'follow_up_suggestions': [
                    'How can I help you today?', 
                    'What would you like to explore?',
                    'Tell me what\'s on your mind!'
                ]
            },
            ConversationState.EMERGENCY_SUPPORT: {
                'tone': 'urgent_supportive',
                'detail_level': 'immediate_care',
                'interaction_style': 'crisis_intervention',
                'emotional_support_level': 'maximum',
                'follow_up_suggestions': [
                    'I\'m here to help. Can you tell me more?',
                    'Would you like me to provide some resources?',
                    'How are you feeling right now?'
                ]
            },
            ConversationState.EMOTIONAL_SUPPORT: {
                'tone': 'empathetic',
                'detail_level': 'supportive',
                'interaction_style': 'compassionate',
                'emotional_support_level': 'high',
                'follow_up_suggestions': [
                    'How are you feeling now?', 
                    'Would you like to talk more about this?',
                    'I\'m here to listen and support you.'
                ]
            },
            ConversationState.PROBLEM_SOLVING: {
                'tone': 'analytical',
                'detail_level': 'comprehensive',
                'interaction_style': 'systematic',
                'technical_level': 'high',
                'follow_up_suggestions': [
                    'Would you like me to break this down further?', 
                    'Shall we try a different approach?',
                    'What specific part is challenging you?'
                ]
            },
            ConversationState.CREATIVE_COLLABORATION: {
                'tone': 'enthusiastic',
                'detail_level': 'inspiring',
                'interaction_style': 'collaborative',
                'follow_up_suggestions': [
                    'What other ideas come to mind?', 
                    'How can we build on this?',
                    'Let\'s explore this creatively!'
                ]
            },
            ConversationState.LEARNING_SESSION: {
                'tone': 'educational',
                'detail_level': 'structured',
                'interaction_style': 'teaching',
                'preferred_response_length': 'detailed',
                'follow_up_suggestions': [
                    'Does this make sense?', 
                    'Would you like to practice this?',
                    'Should we explore this topic deeper?'
                ]
            },
            ConversationState.TECHNICAL_DISCUSSION: {
                'tone': 'analytical',
                'detail_level': 'comprehensive',
                'interaction_style': 'expert',
                'technical_level': 'high',
                'preferred_response_length': 'detailed',
                'follow_up_suggestions': [
                    'Would you like more technical details?',
                    'Should we dive deeper into this concept?',
                    'Any specific implementation questions?'
                ]
            },
            ConversationState.CASUAL_CHAT: {
                'tone': 'friendly',
                'detail_level': 'light',
                'interaction_style': 'conversational',
                'follow_up_suggestions': [
                    'That\'s interesting! Tell me more.',
                    'What do you think about that?',
                    'Sounds like fun!'
                ]
            },
            ConversationState.DEEP_ANALYSIS: {
                'tone': 'thoughtful',
                'detail_level': 'comprehensive',
                'interaction_style': 'analytical',
                'technical_level': 'high',
                'preferred_response_length': 'extensive',
                'follow_up_suggestions': [
                    'Would you like me to analyze this further?',
                    'Should we examine other perspectives?',
                    'What aspects interest you most?'
                ]
            }
        }
        
        # Apply state-specific modifications
        if flow.current_state in state_strategies:
            base_strategy.update(state_strategies[flow.current_state])
        
        # Adjust based on engagement level
        if flow.engagement_level > 0.8:
            base_strategy['detail_level'] = 'comprehensive'
            base_strategy['preferred_response_length'] = 'detailed'
        elif flow.engagement_level < 0.3:
            base_strategy['tone'] = 'encouraging'
            base_strategy['follow_up_suggestions'].append(
                'Is there something specific you\'d like to focus on?'
            )
        
        # Momentum considerations
        if flow.flow_momentum > 0.8:
            base_strategy['interaction_style'] = 'energetic'
            base_strategy['tone'] = 'enthusiastic'
        elif flow.flow_momentum < 0.3:
            base_strategy['transition_hints'].append('Would you like to explore something new?')
        
        # Complexity adjustments
        if message_analysis['complexity_score'] > 0.7:
            base_strategy['technical_level'] = 'high'
            base_strategy['detail_level'] = 'comprehensive'
        elif message_analysis['complexity_score'] < 0.3:
            base_strategy['technical_level'] = 'basic'
            base_strategy['detail_level'] = 'simple'
        
        # Urgency adjustments
        if message_analysis.get('urgency_level', 0) > 0.7:
            base_strategy['tone'] = 'urgent_helpful'
            base_strategy['preferred_response_length'] = 'concise'
        
        return base_strategy
    
    def _get_recommended_actions(self, flow: ConversationFlow) -> List[str]:
        """Get recommended actions based on current flow state"""
        recommendations = []
        
        # Low engagement recommendations
        if flow.engagement_level < 0.3:
            recommendations.extend([
                'Ask open-ended questions',
                'Share interesting facts or stories',
                'Suggest interactive activities'
            ])
        
        # High engagement recommendations
        elif flow.engagement_level > 0.8:
            recommendations.extend([
                'Dive deeper into current topic',
                'Introduce related concepts',
                'Encourage user creativity'
            ])
        
        # State-specific recommendations
        if flow.current_state == ConversationState.LEARNING_SESSION:
            recommendations.extend([
                'Provide examples and exercises',
                'Check understanding regularly',
                'Offer additional resources'
            ])
        elif flow.current_state == ConversationState.PROBLEM_SOLVING:
            recommendations.extend([
                'Break down complex problems',
                'Suggest step-by-step approaches',
                'Offer alternative solutions'
            ])
        
        # Context depth recommendations
        if flow.context_depth > 10:
            recommendations.append('Consider summarizing key points')
        elif flow.context_depth < 3:
            recommendations.append('Encourage more detailed discussion')
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def get_comprehensive_flow_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of user's conversation flow"""
        if user_id not in self.user_flows:
            return {'status': 'no_active_flow'}
        
        flow = self.user_flows[user_id]
        
        # Calculate conversation duration
        total_duration = (datetime.now() - flow.last_transition).total_seconds()
        
        # Get recent conversation patterns
        recent_states = [msg.get('state', '') for msg in list(flow.conversation_history)[-10:]]
        state_distribution = {state: recent_states.count(state) for state in set(recent_states)}
        
        return {
            'user_id': user_id,
            'current_state': flow.current_state.value,
            'previous_state': flow.previous_state.value,
            'personality_mode': flow.personality_mode.value,
            'engagement_metrics': {
                'current_level': round(flow.engagement_level, 3),
                'average_score': round(flow.metrics.engagement_score, 3),
                'flow_momentum': round(flow.flow_momentum, 3)
            },
            'conversation_metrics': {
                'total_messages': flow.metrics.total_messages,
                'context_depth': flow.context_depth,
                'complexity_level': round(flow.metrics.complexity_level, 3),
                'emotional_intensity': round(flow.metrics.emotional_intensity, 3),
                'learning_progress': round(flow.metrics.learning_progress, 3),
                'topic_diversity': flow.metrics.topic_diversity
            },
            'active_topics': flow.topic_thread[-5:] if flow.topic_thread else [],
            'learning_topics': list(flow.learning_topics),
            'pending_topics': flow.pending_topics,
            'user_preferences': flow.user_preferences,
            'conversation_health': self._assess_flow_health(flow),
            'state_distribution': state_distribution,
            'conversation_duration_minutes': round(total_duration / 60, 2),
            'recommended_actions': self._get_recommended_actions(flow),
            'last_update': flow.last_transition.isoformat()
        }
    
    def _assess_flow_health(self, flow: ConversationFlow) -> Dict[str, Any]:
        """Comprehensive assessment of conversation flow health"""
        health_score = 0.0
        health_factors = {}
        
        # Engagement health (40% weight)
        if flow.engagement_level > 0.7:
            engagement_health = 'excellent'
            health_score += 4.0
        elif flow.engagement_level > 0.5:
            engagement_health = 'good'
            health_score += 3.0
        elif flow.engagement_level > 0.3:
            engagement_health = 'moderate'
            health_score += 2.0
        else:
            engagement_health = 'needs_attention'
            health_score += 1.0
        
        health_factors['engagement'] = engagement_health
        
        # Momentum health (30% weight)
        if flow.flow_momentum > 0.6:
            momentum_health = 'excellent'
            health_score += 3.0
        elif flow.flow_momentum > 0.4:
            momentum_health = 'good'
            health_score += 2.25
        elif flow.flow_momentum > 0.2:
            momentum_health = 'moderate'
            health_score += 1.5
        else:
            momentum_health = 'needs_attention'
            health_score += 0.75
        
        health_factors['momentum'] = momentum_health
        
        # Context depth health (20% weight)
        if 5 <= flow.context_depth <= 12:
            context_health = 'excellent'
            health_score += 2.0
        elif 3 <= flow.context_depth <= 15:
            context_health = 'good'
            health_score += 1.5
        elif flow.context_depth > 0:
            context_health = 'moderate'
            health_score += 1.0
        else:
            context_health = 'needs_attention'
            health_score += 0.5
        
        health_factors['context_depth'] = context_health
        
        # Learning progress health (10% weight)
        if flow.metrics.learning_progress > 0.7:
            learning_health = 'excellent'
            health_score += 1.0
        elif flow.metrics.learning_progress > 0.4:
            learning_health = 'good'
            health_score += 0.75
        elif flow.metrics.learning_progress > 0.2:
            learning_health = 'moderate'
            health_score += 0.5
        else:
            learning_health = 'basic'
            health_score += 0.25
        
        health_factors['learning_progress'] = learning_health
        
        # Calculate overall health
        max_score = 10.0
        health_percentage = (health_score / max_score) * 100
        
        if health_percentage >= 85:
            overall_health = 'excellent'
        elif health_percentage >= 70:
            overall_health = 'good'
        elif health_percentage >= 50:
            overall_health = 'moderate'
        else:
            overall_health = 'needs_attention'
        
        return {
            'overall': overall_health,
            'score_percentage': round(health_percentage, 1),
            'factors': health_factors,
            'recommendations': self._get_health_recommendations(health_factors)
        }
    
    def _get_health_recommendations(self, health_factors: Dict[str, str]) -> List[str]:
        """Get health improvement recommendations"""
        recommendations = []
        
        if health_factors.get('engagement') == 'needs_attention':
            recommendations.extend([
                'Increase interactive elements',
                'Ask more engaging questions',
                'Share interesting anecdotes'
            ])
        
        if health_factors.get('momentum') == 'needs_attention':
            recommendations.extend([
                'Maintain conversation rhythm',
                'Respond more promptly',
                'Keep topics flowing naturally'
            ])
        
        if health_factors.get('context_depth') == 'needs_attention':
            recommendations.extend([
                'Encourage deeper discussion',
                'Build on previous topics',
                'Ask follow-up questions'
            ])
        
        if health_factors.get('learning_progress') == 'basic':
            recommendations.extend([
                'Introduce educational elements',
                'Provide learning opportunities',
                'Encourage skill development'
            ])
        
        return recommendations[:3]  # Limit to top 3 recommendations

    # Additional utility methods
    def reset_user_flow(self, user_id: str) -> bool:
        """Reset user's conversation flow"""
        if user_id in self.user_flows:
            del self.user_flows[user_id]
            logger.info(f"Reset conversation flow for user {user_id}")
            return True
        return False
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """Export user's conversation data"""
        if user_id not in self.user_flows:
            return {}
        
        flow = self.user_flows[user_id]
        return {
            'user_id': user_id,
            'conversation_history': list(flow.conversation_history),
            'learning_topics': list(flow.learning_topics),
            'user_preferences': flow.user_preferences,
            'metrics': {
                'total_messages': flow.metrics.total_messages,
                'engagement_score': flow.metrics.engagement_score,
                'complexity_level': flow.metrics.complexity_level,
                'learning_progress': flow.metrics.learning_progress
            },
            'personality_mode': flow.personality_mode.value,
            'export_timestamp': datetime.now().isoformat()
        }
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get overall system statistics"""
        total_users = len(self.user_flows)
        if total_users == 0:
            return {'total_users': 0}
        
        # Calculate aggregate statistics
        total_messages = sum(flow.metrics.total_messages for flow in self.user_flows.values())
        avg_engagement = sum(flow.engagement_level for flow in self.user_flows.values()) / total_users
        
        # State distribution
        state_counts = defaultdict(int)
        for flow in self.user_flows.values():
            state_counts[flow.current_state.value] += 1
        
        # Personality distribution
        personality_counts = defaultdict(int)
        for flow in self.user_flows.values():
            personality_counts[flow.personality_mode.value] += 1
        
        return {
            'total_users': total_users,
            'total_messages': total_messages,
            'average_engagement': round(avg_engagement, 3),
            'state_distribution': dict(state_counts),
            'personality_distribution': dict(personality_counts),
            'system_uptime': datetime.now().isoformat()
        }
