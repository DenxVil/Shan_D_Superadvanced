"""
Tests for Shan-D Core Functionality
Created by: ◉Ɗєиνιℓ 
"""
import pytest
import asyncio
from src.core.shan_d_enhanced import EnhancedShanD
from src.storage.user_data_manager import UserDataManager
from src.core.learning_engine import ContinuousLearningEngine

@pytest.fixture
def shan_d_instance():
    """Create Shan-D instance for testing"""
    user_data_manager = UserDataManager()
    learning_engine = ContinuousLearningEngine()
    return EnhancedShanD(user_data_manager, learning_engine)

@pytest.mark.asyncio
async def test_message_processing(shan_d_instance):
    """Test basic message processing"""
    response = await shan_d_instance.process_message_ultra_human(
        "test_user", "Hello!", {}
    )
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_emotion_analysis(shan_d_instance):
    """Test emotion analysis"""
    # Test happy emotion
    response = await shan_d_instance.process_message_ultra_human(
        "test_user", "I'm so happy today!", {}
    )
    assert "happy" in response.lower() or "great" in response.lower()

@pytest.mark.asyncio
async def test_multilingual_support(shan_d_instance):
    """Test multilingual conversation"""
    # Test Hindi input
    response = await shan_d_instance.process_message_ultra_human(
        "test_user", "नमस्ते! कैसे हो?", {}
    )
    assert isinstance(response, str)
    assert len(response) > 0

def test_analytics_generation(shan_d_instance):
    """Test analytics generation"""
    analytics = asyncio.run(shan_d_instance.get_ultra_human_analytics())
    assert isinstance(analytics, dict)
    assert "ai_personality" in analytics
    assert "created_by" in analytics
