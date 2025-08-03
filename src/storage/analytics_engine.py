"""
Analytics Engine for Shan-D
Created by: ◉Ɗєиνιℓ
Advanced analytics and performance tracking
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiofiles

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    """Advanced analytics and metrics tracking"""
    
    def __init__(self):
        self.analytics_path = Path("data/analytics")
        self.analytics_path.mkdir(exist_ok=True)
        self.metrics_cache = {}
        logger.info("📊 AnalyticsEngine initialized by ◉Ɗєиνιℓ")
    
    async def track_interaction(
        self, 
        user_id: str, 
        interaction_data: Dict
    ):
        """Track user interaction for analytics"""
        
        timestamp = datetime.now()
        analytics_entry = {
            "timestamp": timestamp.isoformat(),
            "user_id": user_id,
            "interaction_type": interaction_data.get("type", "message"),
            "response_time": interaction_data.get("processing_time", 0),
            "satisfaction_score": interaction_data.get("satisfaction", 0.8),
            "language": interaction_data.get("language", "en"),
            "emotion": interaction_data.get("emotion", "neutral")
        }
        
        # Store analytics data
        await self._store_analytics_entry(analytics_entry)
        
        # Update real-time metrics
        await self._update_metrics(analytics_entry)
    
    async def generate_analytics_report(
        self, 
        timeframe: str = "24h"
    ) -> Dict:
        """Generate comprehensive analytics report"""
        
        end_time = datetime.now()
        
        if timeframe == "24h":
            start_time = end_time - timedelta(hours=24)
        elif timeframe == "7d":
            start_time = end_time - timedelta(days=7)
        elif timeframe == "30d":
            start_time = end_time - timedelta(days=30)
        else:
            start_time = end_time - timedelta(hours=24)
        
        # Load analytics data for timeframe
        analytics_data = await self._load_analytics_data(start_time, end_time)
        
        report = {
            "timeframe": timeframe,
            "period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            },
            "total_interactions": len(analytics_data),
            "unique_users": len(set(entry["user_id"] for entry in analytics_data)),
            "average_response_time": self._calculate_average_response_time(analytics_data),
            "user_satisfaction": self._calculate_satisfaction_score(analytics_data),
            "language_breakdown": self._analyze_languages(analytics_data),
            "emotion_analysis": self._analyze_emotions(analytics_data),
            "peak_hours": self._analyze_peak_hours(analytics_data)
        }
        
        return report
    
    async def _store_analytics_entry(self, entry: Dict):
        """Store analytics entry to file"""
        analytics_file = self.analytics_path / f"analytics_{datetime.now().strftime('%Y%m%d')}.json"
        
        async with aiofiles.open(analytics_file, 'a', encoding='utf-8') as f:
            await f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    async def _update_metrics(self, entry: Dict):
        """Update real-time metrics cache"""
        today = datetime.now().strftime('%Y%m%d')
        
        if today not in self.metrics_cache:
            self.metrics_cache[today] = {
                "total_interactions": 0,
                "total_users": set(),
                "total_response_time": 0
            }
        
        metrics = self.metrics_cache[today]
        metrics["total_interactions"] += 1
        metrics["total_users"].add(entry["user_id"])
        metrics["total_response_time"] += entry.get("response_time", 0)
    
    async def _load_analytics_data(self, start_time: datetime, end_time: datetime) -> List[Dict]:
        """Load analytics data for given timeframe"""
        analytics_data = []
        
        # Generate list of dates to check
        current_date = start_time.date()
        end_date = end_time.date()
        
        while current_date <= end_date:
            file_path = self.analytics_path / f"analytics_{current_date.strftime('%Y%m%d')}.json"
            
            if file_path.exists():
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    for line in content.strip().split('\n'):
                        if line.strip():
                            entry = json.loads(line)
                            entry_time = datetime.fromisoformat(entry["timestamp"])
                            if start_time <= entry_time <= end_time:
                                analytics_data.append(entry)
            
            current_date += timedelta(days=1)
        
        return analytics_data
    
    def _calculate_average_response_time(self, data: List[Dict]) -> float:
        """Calculate average response time"""
        if not data:
            return 0.0
        
        total_time = sum(entry.get("response_time", 0) for entry in data)
        return total_time / len(data)
    
    def _calculate_satisfaction_score(self, data: List[Dict]) -> float:
        """Calculate average satisfaction score"""
        if not data:
            return 0.8
        
        total_satisfaction = sum(entry.get("satisfaction_score", 0.8) for entry in data)
        return total_satisfaction / len(data)
    
    def _analyze_languages(self, data: List[Dict]) -> Dict:
        """Analyze language distribution"""
        language_count = {}
        for entry in data:
            lang = entry.get("language", "en")
            language_count[lang] = language_count.get(lang, 0) + 1
        
        return language_count
    
    def _analyze_emotions(self, data: List[Dict]) -> Dict:
        """Analyze emotion distribution"""
        emotion_count = {}
        for entry in data:
            emotion = entry.get("emotion", "neutral")
            emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
        
        return emotion_count
    
    def _analyze_peak_hours(self, data: List[Dict]) -> Dict:
        """Analyze peak usage hours"""
        hour_count = {}
        for entry in data:
            hour = datetime.fromisoformat(entry["timestamp"]).hour
            hour_count[hour] = hour_count.get(hour, 0) + 1
        
        return dict(sorted(hour_count.items()))
