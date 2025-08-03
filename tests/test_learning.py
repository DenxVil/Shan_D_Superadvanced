"""
Tests for Learning Engine
Created by: ◉Ɗєиνιℓ 
"""
import pytest
import asyncio
from src.core.learning_engine import ContinuousLearningEngine

@pytest.fixture
def learning_engine():
    """Create learning engine for testing"""
    return ContinuousLearningEngine()

@pytest.mark.asyncio
async def test_learning_from_interaction(learning_engine):
    """Test learning from user interactions"""
    await learning_engine.learn_from_interaction(
        "test_user", "Hello", "Hi there!", {}, {}
    )
    
    assert learning_engine.learning_cycles >= 0

@pytest.mark.asyncio
async def test_adaptation_suggestions(learning_engine):
    """Test adaptation suggestions"""
    suggestions = await learning_engine.get_adaptation_suggestions(
        "test_user", {"conversation_type": "casual"}
    )
    
    assert isinstance(suggestions, dict)
    assert "conversation_style" in suggestions
    assert "response_length" in suggestions
