import pytest
import asyncio
from src.core.model_manager import AdvancedModelManager
from src.core.error_handler import AdvancedErrorHandler

@pytest.mark.asyncio
async def test_model_manager():
    config = {'openai_api_key': 'test_key'}
    manager = AdvancedModelManager(config)
    await manager.initialize()
    
    # Test model selection
    query = "What is 2+2?"
    context = {}
    model = await manager.select_optimal_model(query, context, {})
    
    assert model is not None
    await manager.close()

@pytest.mark.asyncio
async def test_error_handler():
    config = {'openai_api_key': 'test_key'}
    manager = AdvancedModelManager(config)
    handler = AdvancedErrorHandler(manager)
    
    try:
        raise ValueError("Test error")
    except ValueError as e:
        result = await handler.handle_error(e, {'user_id': 'test'})
        assert result['handled'] == True
        assert 'error_id' in result
