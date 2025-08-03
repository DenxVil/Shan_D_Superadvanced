"""
Advanced Memory Manager for Shan-D
Created by: Dr ◉Ɗєиνιℓ 
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class AdvancedMemoryManager:
    """Advanced memory management with learning capabilities"""
    
    def __init__(self):
        self.memory_cache = {}
        logger.info("🧠 AdvancedMemoryManager initialized by ◉Ɗєиνιℓ 🧑‍💻")
    
    async def store_enhanced_interaction_with_learning(
        self,
        user_id: str,
        message: str,
        response: str,
        emotion_analysis: Dict,
        language: str,
        context: Dict,
        conversation_type: str
    ):
        """Store interaction with enhanced learning capabilities"""
        
        interaction_data = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "message": message,
            "response": response,
            "emotion_analysis": emotion_analysis,
            "language": language,
            "context": context,
            "conversation_type": conversation_type
        }
        
        # Store in memory cache
        if user_id not in self.memory_cache:
            self.memory_cache[user_id] = []
        
        self.memory_cache[user_id].append(interaction_data)
        
        # Keep only last 100 interactions per user
        self.memory_cache[user_id] = self.memory_cache[user_id][-100:]
        
        logger.debug(f"💾 Stored enhanced interaction for user {user_id}")
    
    async def emergency_save(self):
        """Emergency save for shutdown"""
        logger.info("💾 Emergency saving memory data...")
        # Save critical memory data before shutdown



"""
Shan-D Memory Management System
Advanced conversation memory with context persistence and intelligent retrieval
"""

import json
import sqlite3
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import asyncio
import pickle
import os

@dataclass
class MemoryEntry:
    user_id: str
    conversation_id: str
    message_id: str
    content: str
    role: str  # 'user' or 'assistant'
    timestamp: datetime
    emotions: Dict[str, float]
    importance_score: float
    context_tags: List[str]
    metadata: Dict[str, Any]

@dataclass
class ConversationContext:
    user_id: str
    conversation_id: str
    topic: str
    summary: str
    key_points: List[str]
    emotional_tone: str
    start_time: datetime
    last_update: datetime
    message_count: int

class ShanDMemoryManager:
    def __init__(self, db_path: str = "shan_d_memory.db", max_memory_per_user: int = 1000):
        self.db_path = db_path
        self.max_memory_per_user = max_memory_per_user
        self.active_contexts: Dict[str, ConversationContext] = {}
        self.short_term_memory: Dict[str, List[MemoryEntry]] = {}
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for persistent memory storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Memory entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                conversation_id TEXT NOT NULL,
                message_id TEXT NOT NULL,
                content TEXT NOT NULL,
                role TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                emotions TEXT,
                importance_score REAL,
                context_tags TEXT,
                metadata TEXT
            )
        ''')
        
        # Conversation contexts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_contexts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                conversation_id TEXT NOT NULL UNIQUE,
                topic TEXT,
                summary TEXT,
                key_points TEXT,
                emotional_tone TEXT,
                start_time TEXT,
                last_update TEXT,
                message_count INTEGER DEFAULT 0
            )
        ''')
        
        # User profiles table for long-term memory
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                preferences TEXT,
                personality_data TEXT,
                learning_history TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON memory_entries(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversation_id ON memory_entries(conversation_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON memory_entries(timestamp)')
        
        conn.commit()
        conn.close()
    
    async def store_memory(self, memory_entry: MemoryEntry):
        """Store a memory entry in both short-term and long-term memory"""
        # Add to short-term memory
        if memory_entry.user_id not in self.short_term_memory:
            self.short_term_memory[memory_entry.user_id] = []
        
        self.short_term_memory[memory_entry.user_id].append(memory_entry)
        
        # Maintain short-term memory size limit
        if len(self.short_term_memory[memory_entry.user_id]) > 50:
            self.short_term_memory[memory_entry.user_id] = self.short_term_memory[memory_entry.user_id][-50:]
        
        # Store in long-term database
        await self._store_in_database(memory_entry)
        
        # Update conversation context
        await self._update_conversation_context(memory_entry)
    
    async def _store_in_database(self, memory_entry: MemoryEntry):
        """Store memory entry in SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO memory_entries 
                (user_id, conversation_id, message_id, content, role, timestamp, 
                 emotions, importance_score, context_tags, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory_entry.user_id,
                memory_entry.conversation_id,
                memory_entry.message_id,
                memory_entry.content,
                memory_entry.role,
                memory_entry.timestamp.isoformat(),
                json.dumps(memory_entry.emotions),
                memory_entry.importance_score,
                json.dumps(memory_entry.context_tags),
                json.dumps(memory_entry.metadata)
            ))
            
            conn.commit()
            
            # Cleanup old memories if user exceeds limit
            await self._cleanup_old_memories(memory_entry.user_id)
            
        except Exception as e:
            print(f"Error storing memory: {e}")
        finally:
            conn.close()
    
    async def _cleanup_old_memories(self, user_id: str):
        """Remove old memories if user exceeds memory limit"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Count current memories
            cursor.execute('SELECT COUNT(*) FROM memory_entries WHERE user_id = ?', (user_id,))
            count = cursor.fetchone()[0]
            
            if count > self.max_memory_per_user:
                # Keep only the most recent and important memories
                cursor.execute('''
                    DELETE FROM memory_entries 
                    WHERE user_id = ? AND id NOT IN (
                        SELECT id FROM memory_entries 
                        WHERE user_id = ? 
                        ORDER BY importance_score DESC, timestamp DESC 
                        LIMIT ?
                    )
                ''', (user_id, user_id, self.max_memory_per_user))
                
                conn.commit()
        except Exception as e:
            print(f"Error cleaning up memories: {e}")
        finally:
            conn.close()
    
    async def _update_conversation_context(self, memory_entry: MemoryEntry):
        """Update or create conversation context"""
        context_id = memory_entry.conversation_id
        user_id = memory_entry.user_id
        
        if context_id not in self.active_contexts:
            # Create new context
            self.active_contexts[context_id] = ConversationContext(
                user_id=user_id,
                conversation_id=context_id,
                topic=self._extract_topic(memory_entry.content),
                summary="",
                key_points=[],
                emotional_tone=self._determine_emotional_tone(memory_entry.emotions),
                start_time=memory_entry.timestamp,
                last_update=memory_entry.timestamp,
                message_count=1
            )
        else:
            # Update existing context
            context = self.active_contexts[context_id]
            context.last_update = memory_entry.timestamp
            context.message_count += 1
            context.emotional_tone = self._update_emotional_tone(
                context.emotional_tone, 
                self._determine_emotional_tone(memory_entry.emotions)
            )
        
        # Store context in database
        await self._store_conversation_context(self.active_contexts[context_id])
    
    async def retrieve_relevant_memories(self, user_id: str, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Retrieve memories relevant to the current query"""
        # First check short-term memory
        short_term = self._search_short_term_memory(user_id, query)
        
        # Then search long-term database
        long_term = await self._search_database_memory(user_id, query, limit - len(short_term))
        
        # Combine and deduplicate
        all_memories = short_term + long_term
        seen_ids = set()
        unique_memories = []
        
        for memory in all_memories:
            if memory.message_id not in seen_ids:
                unique_memories.append(memory)
                seen_ids.add(memory.message_id)
        
        # Sort by relevance and importance
        unique_memories.sort(key=lambda x: x.importance_score, reverse=True)
        
        return unique_memories[:limit]
    
    def _search_short_term_memory(self, user_id: str, query: str) -> List[MemoryEntry]:
        """Search short-term memory for relevant entries"""
        if user_id not in self.short_term_memory:
            return []
        
        query_words = set(query.lower().split())
        relevant_memories = []
        
        for memory in self.short_term_memory[user_id]:
            content_words = set(memory.content.lower().split())
            # Calculate relevance based on word overlap
            overlap = len(query_words.intersection(content_words))
            if overlap > 0:
                memory.importance_score += overlap * 0.1  # Boost relevance
                relevant_memories.append(memory)
        
        return relevant_memories
    
    async def _search_database_memory(self, user_id: str, query: str, limit: int) -> List[MemoryEntry]:
        """Search database for relevant memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        memories = []
        
        try:
            # Simple keyword search (could be enhanced with vector similarity)
            query_words = query.lower().split()
            search_conditions = []
            search_params = [user_id]
            
            for word in query_words[:5]:  # Limit to 5 keywords for performance
                search_conditions.append("LOWER(content) LIKE ?")
                search_params.append(f"%{word}%")
            
            where_clause = "user_id = ?"
            if search_conditions:
                where_clause += " AND (" + " OR ".join(search_conditions) + ")"
            
            cursor.execute(f'''
                SELECT * FROM memory_entries 
                WHERE {where_clause}
                ORDER BY importance_score DESC, timestamp DESC 
                LIMIT ?
            ''', search_params + [limit])
            
            rows = cursor.fetchall()
            
            for row in rows:
                memory = MemoryEntry(
                    user_id=row[1],
                    conversation_id=row[2],
                    message_id=row[3],
                    content=row[4],
                    role=row[5],
                    timestamp=datetime.fromisoformat(row[6]),
                    emotions=json.loads(row[7]) if row[7] else {},
                    importance_score=row[8],
                    context_tags=json.loads(row[9]) if row[9] else [],
                    metadata=json.loads(row[10]) if row[10] else {}
                )
                memories.append(memory)
                
        except Exception as e:
            print(f"Error searching memory database: {e}")
        finally:
            conn.close()
        
        return memories
    
    async def get_conversation_summary(self, conversation_id: str) -> Optional[str]:
        """Get summary of a conversation"""
        if conversation_id in self.active_contexts:
            return self.active_contexts[conversation_id].summary
        
        # Check database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT summary FROM conversation_contexts WHERE conversation_id = ?',
                (conversation_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error retrieving conversation summary: {e}")
            return None
        finally:
            conn.close()
    
    async def update_conversation_summary(self, conversation_id: str, summary: str):
        """Update conversation summary"""
        if conversation_id in self.active_contexts:
            self.active_contexts[conversation_id].summary = summary
            await self._store_conversation_context(self.active_contexts[conversation_id])
    
    async def _store_conversation_context(self, context: ConversationContext):
        """Store conversation context in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO conversation_contexts
                (user_id, conversation_id, topic, summary, key_points, emotional_tone,
                 start_time, last_update, message_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                context.user_id,
                context.conversation_id,
                context.topic,
                context.summary,
                json.dumps(context.key_points),
                context.emotional_tone,
                context.start_time.isoformat(),
                context.last_update.isoformat(),
                context.message_count
            ))
            
            conn.commit()
        except Exception as e:
            print(f"Error storing conversation context: {e}")
        finally:
            conn.close()
    
    def calculate_importance_score(self, content: str, emotions: Dict[str, float], 
                                 context_tags: List[str]) -> float:
        """Calculate importance score for a memory entry"""
        score = 0.0
        
        # Base score for content length (longer = more important, up to a point)
        content_length = len(content)
        if content_length > 100:
            score += 0.3
        elif content_length > 50:
            score += 0.2
        else:
            score += 0.1
        
        # Emotional intensity adds importance
        if emotions:
            max_emotion = max(emotions.values())
            score += max_emotion * 0.4
        
        # Context tags add importance
        important_tags = ['personal', 'preference', 'goal', 'problem', 'achievement']
        tag_boost = len(set(context_tags).intersection(important_tags)) * 0.1
        score += tag_boost
        
        # Question marks might indicate important queries
        if '?' in content:
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _extract_topic(self, content: str) -> str:
        """Extract topic from message content"""
        # Simple topic extraction (could be enhanced with NLP)
        words = content.lower().split()
        
        # Common topic keywords
        topic_keywords = [
            'help', 'problem', 'question', 'learn', 'teach', 'explain',
            'code', 'programming', 'work', 'project', 'idea', 'advice'
        ]
        
        for keyword in topic_keywords:
            if keyword in words:
                return keyword.title()
        
        # If no specific topic, use first few words
        return ' '.join(words[:3]).title() if words else "General"
    
    def _determine_emotional_tone(self, emotions: Dict[str, float]) -> str:
        """Determine overall emotional tone"""
        if not emotions:
            return "neutral"
        
        max_emotion = max(emotions, key=emotions.get)
        return max_emotion
    
    def _update_emotional_tone(self, current_tone: str, new_tone: str) -> str:
        """Update emotional tone based on new input"""
        # Simple tone blending (could be more sophisticated)
        emotion_weights = {
            'joy': 1.0, 'excitement': 0.9, 'contentment': 0.8,
            'neutral': 0.5,
            'sadness': -0.8, 'anger': -0.9, 'fear': -0.7
        }
        
        current_weight = emotion_weights.get(current_tone, 0.0)
        new_weight = emotion_weights.get(new_tone, 0.0)
        
        # Weighted average with more influence on recent emotion
        blended_weight = (current_weight * 0.3) + (new_weight * 0.7)
        
        # Map back to emotion
        for emotion, weight in emotion_weights.items():
            if abs(blended_weight - weight) < 0.2:
                return emotion
        
        return new_tone  # Fallback to new tone
    
    async def get_user_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get memory statistics for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {
            'total_memories': 0,
            'conversations': 0,
            'average_importance': 0.0,
            'most_common_emotions': [],
            'memory_span_days': 0
        }
        
        try:
            # Total memories
            cursor.execute('SELECT COUNT(*) FROM memory_entries WHERE user_id = ?', (user_id,))
            stats['total_memories'] = cursor.fetchone()[0]
            
            # Conversations
            cursor.execute('SELECT COUNT(DISTINCT conversation_id) FROM memory_entries WHERE user_id = ?', (user_id,))
            stats['conversations'] = cursor.fetchone()[0]
            
            # Average importance
            cursor.execute('SELECT AVG(importance_score) FROM memory_entries WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()[0]
            stats['average_importance'] = round(result, 2) if result else 0.0
            
            # Memory span
            cursor.execute('''
                SELECT MIN(timestamp), MAX(timestamp) 
                FROM memory_entries WHERE user_id = ?
            ''', (user_id,))
            min_time, max_time = cursor.fetchone()
            
            if min_time and max_time:
                min_dt = datetime.fromisoformat(min_time)
                max_dt = datetime.fromisoformat(max_time)
                stats['memory_span_days'] = (max_dt - min_dt).days
            
        except Exception as e:
            print(f"Error getting memory stats: {e}")
        finally:
            conn.close()
        
        return stats
    
    async def clear_conversation_memory(self, conversation_id: str):
        """Clear all memories for a specific conversation"""
        # Remove from active contexts
        if conversation_id in self.active_contexts:
            del self.active_contexts[conversation_id]
        
        # Remove from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM memory_entries WHERE conversation_id = ?', (conversation_id,))
            cursor.execute('DELETE FROM conversation_contexts WHERE conversation_id = ?', (conversation_id,))
            conn.commit()
        except Exception as e:
            print(f"Error clearing conversation memory: {e}")
        finally:
            conn.close()
