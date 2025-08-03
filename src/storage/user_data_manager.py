"""
Advanced User Data Management for Shan-D
Created by: ◉Ɗєиνιℓ
Handles comprehensive user analysis, story generation, and data organization
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiofiles
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    user_id: str
    name: Optional[str] = None
    personality_traits: Dict = None
    communication_style: Dict = None
    emotional_patterns: Dict = None
    interests: List[str] = None
    cultural_context: str = "general"
    language_preferences: List[str] = None
    interaction_count: int = 0
    first_interaction: Optional[datetime] = None
    last_interaction: Optional[datetime] = None
    mood_history: List[Dict] = None
    conversation_topics: List[str] = None
    life_events: List[Dict] = None
    goals_and_aspirations: List[str] = None
    relationship_context: Dict = None
    
    def __post_init__(self):
        if self.personality_traits is None:
            self.personality_traits = {}
        if self.communication_style is None:
            self.communication_style = {}
        if self.emotional_patterns is None:
            self.emotional_patterns = {}
        if self.interests is None:
            self.interests = []
        if self.language_preferences is None:
            self.language_preferences = ["en"]
        if self.mood_history is None:
            self.mood_history = []
        if self.conversation_topics is None:
            self.conversation_topics = []
        if self.life_events is None:
            self.life_events = []
        if self.goals_and_aspirations is None:
            self.goals_and_aspirations = []
        if self.relationship_context is None:
            self.relationship_context = {}

class UserDataManager:
    """Advanced user data management with comprehensive analysis and story generation"""
    
    def __init__(self):
        self.base_path = Path("data/users")
        self.base_path.mkdir(exist_ok=True)
        self.pending_analyses = {}
        self.analysis_queue = asyncio.Queue()
        
        logger.info("📊 UserDataManager initialized by ◉Ɗєиνιℓ")
    
    async def store_conversation_interaction(
        self, 
        user_id: str, 
        message: str, 
        response: str, 
        emotion_data: Dict,
        context: Dict
    ):
        """Store conversation with comprehensive analysis"""
        
        user_dir = self.base_path / user_id
        user_dir.mkdir(exist_ok=True)
        
        # Store raw interaction
        interaction_data = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "response": response,
            "emotion_data": emotion_data,
            "context": context,
            "message_length": len(message),
            "response_length": len(response),
            "conversation_type": context.get("conversation_type", "general")
        }
        
        # Append to chat history
        chat_history_file = user_dir / "chat_history.json"
        await self._append_to_json_file(chat_history_file, interaction_data)
        
        # Update user profile
        await self._update_user_profile(user_id, message, emotion_data, context)
        
        # Queue for analysis
        await self.analysis_queue.put({
            "user_id": user_id,
            "interaction": interaction_data,
            "analysis_type": "conversation"
        })
        
        logger.debug(f"📝 Stored interaction for user {user_id}")
    
    async def generate_user_story_summary(self, user_id: str) -> str:
        """Generate comprehensive story summary of user's journey"""
        
        profile = await self.get_user_profile(user_id)
        chat_history = await self.get_chat_history(user_id, limit=50)
        
        if not chat_history:
            return "This user is just beginning their journey with Shan-D. Looking forward to learning more about them!"
        
        # Generate narrative story
        story = await self._compose_user_story(user_id, profile)
        
        # Save story
        story_file = self.base_path / user_id / "story_summary.txt"
        async with aiofiles.open(story_file, 'w', encoding='utf-8') as f:
            await f.write(story)
        
        return story
    
    async def _compose_user_story(self, user_id: str, profile: UserProfile) -> str:
        """Compose a narrative story about the user"""
        
        name = profile.name or "this wonderful person"
        interaction_count = profile.interaction_count
        duration = self._calculate_interaction_duration(profile)
        
        story = f"""
📖 **{name}'s Journey with Shan-D**
*A Story by ◉Ɗєиνιℓ AI Technology*

{name} has been engaging with Shan-D for {duration}. They show consistent interest in meaningful conversation and personal growth.

**Personality & Character:**
{name} shows genuine curiosity and openness in our conversations. They communicate naturally and seem to value authentic connection.

**Our Journey Together:**
Over {duration}, we've shared {interaction_count} meaningful conversations. Each interaction has helped me understand {name} better and provide more personalized support. Their unique personality, interests, and communication style make every conversation special.

*This story continues to evolve with every conversation we share.*

---
*Generated by Shan-D AI Assistant*
*Created with ❤️ by ◉Ɗєиνιℓ Advanced AI Technology*
        """
        
        return story.strip()
    
    async def get_user_profile(self, user_id: str) -> UserProfile:
        """Get user profile, create if doesn't exist"""
        profile_file = self.base_path / user_id / "profile.json"
        
        if profile_file.exists():
            async with aiofiles.open(profile_file, 'r', encoding='utf-8') as f:
                data = json.loads(await f.read())
                # Convert datetime strings back to datetime objects
                if data.get('first_interaction'):
                    data['first_interaction'] = datetime.fromisoformat(data['first_interaction'])
                if data.get('last_interaction'):
                    data['last_interaction'] = datetime.fromisoformat(data['last_interaction'])
                return UserProfile(user_id=user_id, **data)
        else:
            return UserProfile(user_id=user_id)
    
    async def get_chat_history(self, user_id: str, limit: Optional[int] = None) -> List[Dict]:
        """Get chat history for user"""
        chat_file = self.base_path / user_id / "chat_history.json"
        
        if not chat_file.exists():
            return []
        
        async with aiofiles.open(chat_file, 'r', encoding='utf-8') as f:
            content = await f.read()
            if not content.strip():
                return []
            
            history = []
            for line in content.strip().split('\n'):
                if line.strip():
                    history.append(json.loads(line))
            
            if limit:
                return history[-limit:]
            return history
    
    async def get_user_key_information(self, user_id: str) -> Dict:
        """Get key information summary about user"""
        
        profile = await self.get_user_profile(user_id)
        
        # Extract most important information
        key_info = {
            "name": profile.name,
            "personality_highlights": "Developing understanding",
            "current_mood_trend": "Balanced",
            "primary_interests": profile.interests[:5],  # Top 5 interests
            "communication_style": "Natural and engaging",
            "cultural_context": profile.cultural_context,
            "preferred_languages": profile.language_preferences,
            "relationship_status": profile.relationship_context.get("status", "unknown"),
            "recent_topics": profile.conversation_topics[-10:],  # Last 10 topics
            "goals": profile.goals_and_aspirations[:3],  # Top 3 goals
            "interaction_summary": {
                "total_conversations": profile.interaction_count,
                "average_mood": "positive",
                "most_discussed_topic": "general conversation"
            }
        }
        
        # Save key info
        key_info_file = self.base_path / user_id / "key_information.json"
        async with aiofiles.open(key_info_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(key_info, indent=2, ensure_ascii=False))
        
        return key_info
    
    async def periodic_user_analysis(self):
        """Periodic background analysis of users"""
        while True:
            try:
                # Process analysis queue
                while not self.analysis_queue.empty():
                    analysis_task = await self.analysis_queue.get()
                    await self._process_analysis_task(analysis_task)
                
                # Periodic comprehensive analysis for active users
                await self._run_periodic_comprehensive_analysis()
                
            except Exception as e:
                logger.error(f"Error in periodic user analysis: {e}")
            
            # Wait before next cycle
            await asyncio.sleep(300)  # Every 5 minutes
    
    async def save_all_pending_data(self):
        """Save all pending data on shutdown"""
        logger.info("💾 Saving all pending user data...")
        # Process remaining analysis queue
        while not self.analysis_queue.empty():
            try:
                analysis_task = await self.analysis_queue.get()
                await self._process_analysis_task(analysis_task)
            except Exception as e:
                logger.error(f"Error processing pending analysis: {e}")
    
    # Helper methods
    async def _append_to_json_file(self, file_path: Path, data: Dict):
        """Append data to JSON lines file"""
        async with aiofiles.open(file_path, 'a', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    def _calculate_interaction_duration(self, profile: UserProfile) -> str:
        """Calculate how long user has been interacting"""
        if not profile.first_interaction:
            return "just started"
        
        duration = datetime.now() - profile.first_interaction
        
        if duration.days == 0:
            return "today"
        elif duration.days == 1:
            return "1 day"
        elif duration.days < 7:
            return f"{duration.days} days"
        elif duration.days < 30:
            weeks = duration.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''}"
        else:
            months = duration.days // 30
            return f"{months} month{'s' if months > 1 else ''}"
    
    async def _update_user_profile(self, user_id: str, message: str, emotion_data: Dict, context: Dict):
        """Update user profile with new interaction data"""
        profile = await self.get_user_profile(user_id)
        
        # Update basic info
        profile.interaction_count += 1
        profile.last_interaction = datetime.now()
        if profile.first_interaction is None:
            profile.first_interaction = datetime.now()
        
        # Update emotional patterns
        if emotion_data:
            mood_entry = {
                "timestamp": datetime.now().isoformat(),
                "emotion": emotion_data.get("emotion", "neutral"),
                "intensity": emotion_data.get("intensity", 0.5),
                "confidence": emotion_data.get("confidence", 0.5)
            }
            profile.mood_history.append(mood_entry)
            # Keep only last 100 mood entries
            profile.mood_history = profile.mood_history[-100:]
        
        # Save updated profile
        await self._save_user_profile(user_id, profile)
    
    async def _save_user_profile(self, user_id: str, profile: UserProfile):
        """Save user profile to file"""
        user_dir = self.base_path / user_id
        user_dir.mkdir(exist_ok=True)
        
        profile_file = user_dir / "profile.json"
        profile_dict = asdict(profile)
        
        # Convert datetime objects to strings
        if profile_dict.get('first_interaction'):
            profile_dict['first_interaction'] = profile_dict['first_interaction'].isoformat()
        if profile_dict.get('last_interaction'):
            profile_dict['last_interaction'] = profile_dict['last_interaction'].isoformat()
        
        async with aiofiles.open(profile_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(profile_dict, indent=2, ensure_ascii=False))
    
    async def _process_analysis_task(self, task: Dict):
        """Process a single analysis task"""
        try:
            user_id = task['user_id']
            analysis_type = task['analysis_type']
            
            if analysis_type == "conversation":
                # Update user analysis based on conversation
                await self.analyze_user_comprehensive(user_id)
            
        except Exception as e:
            logger.error(f"Error processing analysis task: {e}")
    
    async def analyze_user_comprehensive(self, user_id: str) -> Dict:
        """Generate comprehensive user analysis"""
        
        profile = await self.get_user_profile(user_id)
        chat_history = await self.get_chat_history(user_id)
        
        analysis = {
            "user_id": user_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "basic_info": {
                "name": profile.name,
                "interaction_count": profile.interaction_count,
                "first_interaction": profile.first_interaction.isoformat() if profile.first_interaction else None,
                "last_interaction": profile.last_interaction.isoformat() if profile.last_interaction else None
            },
            "personality_analysis": "Developing understanding of user personality",
            "emotional_patterns": "Learning emotional patterns from conversations",
            "communication_preferences": "Adapting to user's communication style",
            "interests_and_topics": profile.interests[:10] if profile.interests else [],
            "recommendations": "Continue natural conversation to learn more"
        }
        
        # Save analysis
        analysis_file = self.base_path / user_id / "user_analysis.json"
        async with aiofiles.open(analysis_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(analysis, indent=2, ensure_ascii=False))
        
        return analysis
    
    async def _run_periodic_comprehensive_analysis(self):
        """Run comprehensive analysis for active users"""
        # Get list of users who have been active recently
        current_time = datetime.now()
        
        for user_dir in self.base_path.iterdir():
            if user_dir.is_dir():
                user_id = user_dir.name
                profile = await self.get_user_profile(user_id)
                
                # Analyze users who have been active in the last 24 hours
                if (profile.last_interaction and 
                    current_time - profile.last_interaction < timedelta(hours=24)):
                    
                    # Generate story summary if it's been a while
                    story_file = user_dir / "story_summary.txt"
                    if (not story_file.exists() or 
                        datetime.now() - datetime.fromtimestamp(story_file.stat().st_mtime) > timedelta(hours=6)):
                        await self.generate_user_story_summary(user_id)
                    
                    # Update key information
                    await self.get_user_key_information(user_id)
