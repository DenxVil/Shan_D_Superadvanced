
#Denvil

"""
Shan-D Conversation Flow Manager
Manages natural conversation flow, context switching, and dialogue coherence
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime, timedelta

class ConversationState(Enum):
    GREETING = "greeting"
    ACTIVE = "active"
    QUESTION_ANSWERING = "question_answering"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVE_COLLABORATION = "creative_collaboration"
    EMOTIONAL_SUPPORT = "emotional_support"
    LEARNING_SESSION = "learning_session"
    WRAPPING_UP = "wrapping_up"
    IDLE = "idle"

class FlowTransition(Enum):
    CONTINUE = "continue"
    ESCALATE = "escalate"
    PIVOT = "pivot"
    CONCLUDE = "conclude"
    RESET = "reset"

@dataclass
class ConversationFlow:
    user_id: str
    current_state: ConversationState
    previous_state: ConversationState
    context_depth: int
    topic_thread: List[str]
    engagement_level: float
    flow_momentum: float
    last_transition: datetime
    pending_topics: List[str]

class ShanDConversationFlow:
    def __init__(self):
        self.user_flows: Dict[str, ConversationFlow] = {}
        self.state_transitions = self._init_state_transitions()
        self.engagement_indicators = self._init_engagement_indicators()
        
    def _init_state_transitions(self) -> Dict[ConversationState, List[ConversationState]]:
        """Initialize valid state transitions"""
        return {
            ConversationState.GREETING: [
                ConversationState.ACTIVE,
                ConversationState.QUESTION_ANSWERING,
                ConversationState.EMOTIONAL_SUPPORT
            ],
            ConversationState.ACTIVE: [
                ConversationState.QUESTION_ANSWERING,
                ConversationState.PROBLEM_SOLVING,
                ConversationState.CREATIVE_COLLABORATION,
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.LEARNING_SESSION,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.QUESTION_ANSWERING: [
                ConversationState.ACTIVE,
                ConversationState.PROBLEM_SOLVING,
                ConversationState.LEARNING_SESSION,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.PROBLEM_SOLVING: [
                ConversationState.ACTIVE,
                ConversationState.CREATIVE_COLLABORATION,
                ConversationState.LEARNING_SESSION,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.CREATIVE_COLLABORATION: [
                ConversationState.ACTIVE,
                ConversationState.PROBLEM_SOLVING,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.EMOTIONAL_SUPPORT: [
                ConversationState.ACTIVE,
                ConversationState.WRAPPING_UP,
                ConversationState.IDLE
            ],
            ConversationState.LEARNING_SESSION: [
                ConversationState.ACTIVE,
                ConversationState.QUESTION_ANSWERING,
                ConversationState.WRAPPING_UP
            ],
            ConversationState.WRAPPING_UP: [
                ConversationState.IDLE,
                ConversationState.ACTIVE
            ],
            ConversationState.IDLE: [
                ConversationState.GREETING,
                ConversationState.ACTIVE
            ]
        }
    
    def _init_engagement_indicators(self) -> Dict[str, Dict[str, float]]:
        """Initialize engagement level indicators"""
        return {
            'high_engagement': {
                'multiple_questions': 0.8,
                'detailed_responses': 0.7,
                'follow_up_questions': 0.9,
                'personal_sharing': 0.8,
                'enthusiasm_markers': 0.6
            },
            'medium_engagement': {
                'single_questions': 0.5,
                'brief_responses': 0.4,
                'acknowledgments': 0.3,
                'topic_continuation': 0.5
            },
            'low_engagement': {
                'short_answers': 0.2,
                'topic_changes': 0.1,
                'delayed_responses': 0.1,
                'generic_responses': 0.2
            }
        }
    
    def get_user_flow(self, user_id: str) -> ConversationFlow:
        """Get or create conversation flow for user"""
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
                pending_topics=[]
            )
        return self.user_flows[user_id]
    
    async def process_message_flow(self, user_id: str, message: str, 
                                 emotion_data: Dict[str, Any], 
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Process message and update conversation flow"""
        flow = self.get_user_flow(user_id)
        
        # Analyze message characteristics
        message_analysis = self._analyze_message(message)
        
        # Update engagement level
        flow.engagement_level = self._calculate_engagement(
            flow.engagement_level, 
            message_analysis, 
            emotion_data
        )
        
        # Determine appropriate state transition
        new_state = await self._determine_state_transition(
            flow, message_analysis, emotion_data, context
        )
        
        # Update flow state
        if new_state != flow.current_state:
            flow.previous_state = flow.current_state
            flow.current_state = new_state
            flow.last_transition = datetime.now()
        
        # Update context depth and topic thread
        self._update_context_tracking(flow, message_analysis)
        
        # Calculate flow momentum
        flow.flow_momentum = self._calculate_momentum(flow, message_analysis)
        
        # Generate flow-appropriate response strategy
        response_strategy = self._generate_response_strategy(flow, message_analysis)
        
        return {
            'current_state': flow.current_state.value,
            'engagement_level': flow.engagement_level,
            'flow_momentum': flow.flow_momentum,
            'context_depth': flow.context_depth,
            'response_strategy': response_strategy,
            'topic_thread': flow.topic_thread[-3:],  # Last 3 topics
            'pending_topics': flow.pending_topics
        }
    
    def _analyze_message(self, message: str) -> Dict[str, Any]:
        """Analyze message characteristics for flow processing"""
        analysis = {
            'length': len(message),
            'word_count': len(message.split()),
            'question_count': message.count('?'),
            'exclamation_count': message.count('!'),
            'has_code': '```
            'has_personal_info': any(word in message.lower() for word in ['i am', 'my', 'me', 'personally']),
            'has_problem': any(word in message.lower() for word in ['problem', 'issue', 'help', 'stuck', 'error']),
            'has_creative_request': any(word in message.lower() for word in ['create', 'design', 'brainstorm', 'idea']),
            'has_learning_intent': any(word in message.lower() for word in ['learn', 'teach', 'explain', 'understand', 'how']),
            'has_emotional_content': any(word in message.lower() for word in ['feel', 'sad', 'happy', 'worried', 'excited']),
            'complexity_score': self._calculate_complexity(message)
        }
        
        return analysis
    
    def _calculate_complexity(self, message: str) -> float:
        """Calculate message complexity score"""
        words = message.split()
        if not words:
            return 0.0
        
        # Factors contributing to complexity
        avg_word_length = sum(len(word) for word in words) / len(words)
        sentence_count = len([s for s in message.split('.') if s.strip()])
        technical_terms = len([word for word in words if len(word) > 8])
        
        complexity = (avg_word_length / 10) + (len(words) / 100) + (technical_terms / len(words))
        
        return min(complexity, 1.0)
    
    def _calculate_engagement(self, current_engagement: float, 
                           message_analysis: Dict[str, Any], 
                           emotion_data: Dict[str, Any]) -> float:
        """Calculate updated engagement level"""
        engagement_delta = 0.0
        
        # Message length and detail boost engagement
        if message_analysis['word_count'] > 20:
            engagement_delta += 0.1
        elif message_analysis['word_count'] < 5:
            engagement_delta -= 0.1
        
        # Questions indicate high engagement
        engagement_delta += message_analysis['question_count'] * 0.15
        
        # Personal information sharing boosts engagement
        if message_analysis['has_personal_info']:
            engagement_delta += 0.2
        
        # Complex messages indicate engagement
        engagement_delta += message_analysis['complexity_score'] * 0.1
        
        # Emotional intensity affects engagement
        if emotion_data and 'intensity' in emotion_data:
            engagement_delta += emotion_data['intensity'] * 0.1
        
        # Update with momentum consideration
        new_engagement = current_engagement + (engagement_delta * 0.7)  # Smooth changes
        
        return max(0.0, min(1.0, new_engagement))
    
    async def _determine_state_transition(self, flow: ConversationFlow,
                                        message_analysis: Dict[str, Any],
                                        emotion_data: Dict[str, Any],
                                        context: Dict[str, Any]) -> ConversationState:
        """Determine appropriate state transition"""
        current_state = flow.current_state
        
        # Emotional support takes priority
        if emotion_data.get('primary_emotion') in ['sadness', 'anger', 'fear', 'anxiety']:
            if emotion_data.get('intensity', 0) > 0.6:
                return ConversationState.EMOTIONAL_SUPPORT
        
        # State-specific transition logic
        if current_state == ConversationState.GREETING:
            if message_analysis['has_problem']:
                return ConversationState.PROBLEM_SOLVING
            elif message_analysis['has_learning_intent']:
                return ConversationState.LEARNING_SESSION
            elif message_analysis['has_creative_request']:
                return ConversationState.CREATIVE_COLLABORATION
            elif message_analysis['question_count'] > 0:
                return ConversationState.QUESTION_ANSWERING
            else:
                return ConversationState.ACTIVE
        
        elif current_state == ConversationState.ACTIVE:
            if message_analysis['has_problem']:
                return ConversationState.PROBLEM_SOLVING
            elif message_analysis['has_creative_request']:
                return ConversationState.CREATIVE_COLLABORATION
            elif message_analysis['has_learning_intent']:
                return ConversationState.LEARNING_SESSION
            elif message_analysis['question_count'] > 0:
                return ConversationState.QUESTION_ANSWERING
        
        # Check for conversation wrap-up signals
        wrap_up_signals = ['thanks', 'thank you', 'that\'s all', 'goodbye', 'bye', 'see you']
        if any(signal in context.get('message', '').lower() for signal in wrap_up_signals):
            if current_state != ConversationState.WRAPPING_UP:
                return ConversationState.WRAPPING_UP
        
        # Check for flow momentum decline
        if flow.flow_momentum < 0.2 and flow.engagement_level < 0.3:
            time_since_transition = datetime.now() - flow.last_transition
            if time_since_transition > timedelta(minutes=5):
                return ConversationState.WRAPPING_UP
        
        return current_state  # No transition needed
    
    def _update_context_tracking(self, flow: ConversationFlow, message_analysis: Dict[str, Any]):
        """Update context depth and topic thread"""
        # Increment context depth for complex/detailed messages
        if message_analysis['complexity_score'] > 0.5 or message_analysis['word_count'] > 30:
            flow.context_depth = min(flow.context_depth + 1, 10)
        elif message_analysis['word_count'] < 10:
            flow.context_depth = max(flow.context_depth - 1, 0)
        
        # Extract and track topics (simplified approach)
        potential_topics = []
        if message_analysis['has_problem']:
            potential_topics.append('problem_solving')
        if message_analysis['has_creative_request']:
            potential_topics.append('creativity')
        if message_analysis['has_learning_intent']:
            potential_topics.append('learning')
        if message_analysis['has_code']:
            potential_topics.append('programming')
        
        # Add new topics to thread
        for topic in potential_topics:
            if topic not in flow.topic_thread[-3:]:  # Avoid immediate duplicates
                flow.topic_thread.append(topic)
        
        # Keep topic thread manageable
        if len(flow.topic_thread) > 10:
            flow.topic_thread = flow.topic_thread[-10:]
    
    def _calculate_momentum(self, flow: ConversationFlow, message_analysis: Dict[str, Any]) -> float:
        """Calculate conversation flow momentum"""
        base_momentum = 0.5
        
        # High engagement boosts momentum
        momentum_boost = flow.engagement_level * 0.3
        
        # Context depth indicates sustained conversation
        context_boost = min(flow.context_depth / 10, 0.2)
        
        # Question asking maintains momentum
        question_boost = message_analysis['question_count'] * 0.1
        
        # Recent activity boosts momentum
        time_since_transition = datetime.now() - flow.last_transition
        if time_since_transition < timedelta(minutes=2):
            recency_boost = 0.2
        else:
            recency_boost = max(0, 0.2 - (time_since_transition.seconds / 600))  # Decay over 10 minutes
        
        total_momentum = base_momentum + momentum_boost + context_boost + question_boost + recency_boost
        
        return max(0.0, min(1.0, total_momentum))
    
    def _generate_response_strategy(self, flow: ConversationFlow, 
                                  message_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response strategy based on current flow"""
        strategy = {
            'tone': 'balanced',
            'detail_level': 'medium',
            'interaction_style': 'collaborative',
            'follow_up_suggestions': [],
            'transition_hints': []
        }
        
        # State-specific strategies
        if flow.current_state == ConversationState.GREETING:
            strategy.update({
                'tone': 'welcoming',
                'interaction_style': 'friendly',
                'follow_up_suggestions': ['How can I help you today?', 'What would you like to explore?']
            })
        
        elif flow.current_state == ConversationState.EMOTIONAL_SUPPORT:
            strategy.update({
                'tone': 'empathetic',
                'detail_level': 'supportive',
                'interaction_style': 'compassionate',
                'follow_up_suggestions': ['How are you feeling now?', 'Would you like to talk more about this?']
            })
        
        elif flow.current_state == ConversationState.PROBLEM_SOLVING:
            strategy.update({
                'tone': 'analytical',
                'detail_level': 'comprehensive',
                'interaction_style': 'systematic',
                'follow_up_suggestions': ['Would you like me to break this down further?', 'Shall we try a different approach?']
            })
        
        elif flow.current_state == ConversationState.CREATIVE_COLLABORATION:
            strategy.update({
                'tone': 'enthusiastic',
                'detail_level': 'inspiring',
                'interaction_style': 'collaborative',
                'follow_up_suggestions': ['What other ideas come to mind?', 'How can we build on this?']
            })
        
        elif flow.current_state == ConversationState.LEARNING_SESSION:
            strategy.update({
                'tone': 'educational',
                'detail_level': 'structured',
                'interaction_style': 'teaching',
                'follow_up_suggestions': ['Does this make sense?', 'Would you like to practice this?']
            })
        
        # Adjust based on engagement level
        if flow.engagement_level > 0.7:
            strategy['detail_level'] = 'comprehensive'
            strategy['interaction_style'] = 'dynamic'
        elif flow.engagement_level < 0.3:
            strategy['tone'] = 'encouraging'
            strategy['follow_up_suggestions'].append('Is there something specific you\'d like to focus on?')
        
        # Momentum considerations
        if flow.flow_momentum > 0.7:
            strategy['interaction_style'] = 'energetic'
        elif flow.flow_momentum < 0.3:
            strategy['transition_hints'].append('Would you like to explore something new?')
        
        return strategy
    
    def get_flow_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's conversation flow"""
        if user_id not in self.user_flows:
            return {'status': 'no_active_flow'}
        
        flow = self.user_flows[user_id]
        
        return {
            'current_state': flow.current_state.value,
            'engagement_level': round(flow.engagement_level, 2),
            'flow_momentum': round(flow.flow_momentum, 2),
            'context_depth': flow.context_depth,
            'active_topics': flow.topic_thread[-3:] if flow.topic_thread else [],
            'conversation_duration': (datetime.now() - flow.last_transition).seconds,
            'flow_health': self._assess_flow_health(flow)
        }
    
    def _assess_flow_health(self, flow: ConversationFlow) -> str:
        """Assess overall health of conversation flow"""
        if flow.engagement_level > 0.7 and flow.flow_momentum > 0.6:
            return 'excellent'
        elif flow.engagement_level > 0.5 and flow.flow_momentum > 0.4:
            return 'good'
        elif flow.engagement_level > 0.3 or flow.flow_momentum > 0.3:
            return 'moderate'
        else:
            return 'needs_attention'
