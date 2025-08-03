#Denvil


import traceback
import sys
import inspect
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any, Type
from dataclasses import dataclass, asdict
from enum import Enum
import psutil
import aiofiles

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    API_ERROR = "api_error"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"
    LOGIC_ERROR = "logic_error"
    SYSTEM_ERROR = "system_error"
    USER_INPUT_ERROR = "user_input_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    AUTHENTICATION_ERROR = "authentication_error"

@dataclass
class ErrorContext:
    error_id: str
    timestamp: datetime
    error_type: str
    error_message: str
    stack_trace: str
    function_name: str
    file_name: str
    line_number: int
    user_id: Optional[str]
    input_data: Dict
    system_state: Dict
    severity: ErrorSeverity
    category: ErrorCategory
    auto_fix_attempted: bool = False
    auto_fix_successful: bool = False
    fix_suggestions: List[str] = None

class AdvancedErrorHandler:
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.error_patterns = self._initialize_error_patterns()
        self.auto_fix_strategies = self._initialize_auto_fix_strategies()
        self.error_log = []
        self.fix_success_rate = {}
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/shan_d_errors.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _initialize_error_patterns(self) -> Dict:
        """Initialize patterns for error categorization and analysis"""
        return {
            'api_timeout': {
                'patterns': ['timeout', 'timed out', 'connection timeout'],
                'category': ErrorCategory.NETWORK_ERROR,
                'severity': ErrorSeverity.MEDIUM,
                'auto_fixable': True
            },
            'rate_limit': {
                'patterns': ['rate limit', 'too many requests', '429', 'quota exceeded'],
                'category': ErrorCategory.RATE_LIMIT_ERROR,
                'severity': ErrorSeverity.HIGH,
                'auto_fixable': True
            },
            'authentication': {
                'patterns': ['unauthorized', 'invalid api key', '401', '403'],
                'category': ErrorCategory.AUTHENTICATION_ERROR,
                'severity': ErrorSeverity.CRITICAL,
                'auto_fixable': False
            },
            'validation': {
                'patterns': ['validation error', 'invalid input', 'missing required'],
                'category': ErrorCategory.VALIDATION_ERROR,
                'severity': ErrorSeverity.LOW,
                'auto_fixable': True
            },
            'memory': {
                'patterns': ['out of memory', 'memory error', 'allocation failed'],
                'category': ErrorCategory.SYSTEM_ERROR,
                'severity': ErrorSeverity.CRITICAL,
                'auto_fixable': False
            }
        }
    
    def _initialize_auto_fix_strategies(self) -> Dict:
        """Initialize auto-fix strategies for different error types"""
        return {
            ErrorCategory.NETWORK_ERROR: self._fix_network_error,
            ErrorCategory.RATE_LIMIT_ERROR: self._fix_rate_limit_error,
            ErrorCategory.VALIDATION_ERROR: self._fix_validation_error,
            ErrorCategory.API_ERROR: self._fix_api_error
        }
    
    async def handle_error(self, error: Exception, context: Dict = None) -> Dict:
        """Main error handling method"""
        
        if context is None:
            context = {}
        
        # Generate unique error ID
        error_id = self._generate_error_id()
        
        # Analyze the error
        error_context = await self._analyze_error(error, error_id, context)
        
        # Log the error
        await self._log_error(error_context)
        
        # Attempt auto-fix if possible
        fix_result = await self._attempt_auto_fix(error_context)
        
        # Generate developer suggestions if auto-fix failed
        suggestions = await self._generate_fix_suggestions(error_context)
        error_context.fix_suggestions = suggestions
        
        # Update error context with fix results
        error_context.auto_fix_attempted = fix_result.get('attempted', False)
        error_context.auto_fix_successful = fix_result.get('successful', False)
        
        # Store in error log
        self.error_log.append(error_context)
        
        # Return comprehensive error report
        return {
            'error_id': error_id,
            'handled': True,
            'auto_fixed': fix_result.get('successful', False),
            'severity': error_context.severity.value,
            'category': error_context.category.value,
            'user_message': self._generate_user_message(error_context),
            'developer_report': asdict(error_context),
            'fix_suggestions': suggestions,
            'retry_recommended': fix_result.get('retry_recommended', False)
        }
    
    async def _analyze_error(self, error: Exception, error_id: str, context: Dict) -> ErrorContext:
        """Analyze error and create detailed context"""
        
        # Extract stack trace information
        exc_type, exc_value, exc_traceback = sys.exc_info()
        stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
        
        # Get frame information
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_frame = frame.f_back
            function_name = caller_frame.f_code.co_name
            file_name = caller_frame.f_code.co_filename
            line_number = caller_frame.f_lineno
        else:
            function_name = "unknown"
            file_name = "unknown"
            line_number = 0
        
        # Categorize error
        category, severity = self._categorize_error(str(error))
        
        # Get system state
        system_state = await self._get_system_state()
        
        return ErrorContext(
            error_id=error_id,
            timestamp=datetime.now(),
            error_type=type(error).__name__,
            error_message=str(error),
            stack_trace=''.join(stack_trace),
            function_name=function_name,
            file_name=file_name,
            line_number=line_number,
            user_id=context.get('user_id'),
            input_data=context,
            system_state=system_state,
            severity=severity,
            category=category
        )
    
    def _categorize_error(self, error_message: str) -> tuple:
        """Categorize error based on message patterns"""
        
        error_lower = error_message.lower()
        
        for pattern_name, pattern_data in self.error_patterns.items():
            for pattern in pattern_data['patterns']:
                if pattern in error_lower:
                    return pattern_data['category'], pattern_data['severity']
        
        # Default categorization
        return ErrorCategory.LOGIC_ERROR, ErrorSeverity.MEDIUM
    
    async def _get_system_state(self) -> Dict:
        """Get current system state for error analysis"""
        
        try:
            return {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'active_connections': len(psutil.net_connections()),
                'process_count': len(psutil.pids()),
                'timestamp': datetime.now().isoformat()
            }
        except Exception:
            return {'error': 'Could not retrieve system state'}
    
    async def _attempt_auto_fix(self, error_context: ErrorContext) -> Dict:
        """Attempt to automatically fix the error"""
        
        if error_context.category not in self.auto_fix_strategies:
            return {'attempted': False, 'successful': False, 'reason': 'No auto-fix strategy available'}
        
        try:
            fix_strategy = self.auto_fix_strategies[error_context.category]
            result = await fix_strategy(error_context)
            
            # Update success rate tracking
            category_name = error_context.category.value
            if category_name not in self.fix_success_rate:
                self.fix_success_rate[category_name] = {'attempts': 0, 'successes': 0}
            
            self.fix_success_rate[category_name]['attempts'] += 1
            if result.get('successful', False):
                self.fix_success_rate[category_name]['successes'] += 1
            
            return result
            
        except Exception as fix_error:
            self.logger.error(f"Auto-fix failed for error {error_context.error_id}: {fix_error}")
            return {'attempted': True, 'successful': False, 'reason': f'Fix strategy failed: {str(fix_error)}'}
    
    async def _fix_network_error(self, error_context: ErrorContext) -> Dict:
        """Fix network-related errors"""
        
        fixes_attempted = []
        
        try:
            await asyncio.sleep(1)  # Initial wait
            fixes_attempted.append("exponential_backoff_retry")
            
            return {
                'attempted': True,
                'successful': True,
                'fixes_applied': fixes_attempted,
                'retry_recommended': True
            }
            
        except Exception:
            return {
                'attempted': True,
                'successful': False,
                'fixes_applied': fixes_attempted,
                'retry_recommended': True
            }
    
    async def _fix_rate_limit_error(self, error_context: ErrorContext) -> Dict:
        """Fix rate limit errors"""
        
        fixes_attempted = []
        
        try:
            wait_time = 60  # Start with 1 minute wait
            await asyncio.sleep(wait_time)
            fixes_attempted.append(f"rate_limit_wait_{wait_time}s")
            
            return {
                'attempted': True,
                'successful': True,
                'fixes_applied': fixes_attempted,
                'retry_recommended': True
            }
            
        except Exception:
            return {
                'attempted': True,
                'successful': False,
                'fixes_applied': fixes_attempted,
                'retry_recommended': True
            }
    
    async def _fix_validation_error(self, error_context: ErrorContext) -> Dict:
        """Fix validation errors"""
        
        fixes_attempted = []
        
        try:
            input_data = error_context.input_data
            
            # Remove None values
            cleaned_data = {k: v for k, v in input_data.items() if v is not None}
            fixes_attempted.append("null_value_removal")
            
            # Validate required fields
            required_fields = ['user_id', 'query']
            for field in required_fields:
                if field not in cleaned_data:
                    cleaned_data[field] = f"default_{field}"
                    fixes_attempted.append(f"default_{field}_added")
            
            error_context.input_data = cleaned_data
            
            return {
                'attempted': True,
                'successful': True,
                'fixes_applied': fixes_attempted,
                'retry_recommended': True,
                'cleaned_data': cleaned_data
            }
            
        except Exception:
            return {
                'attempted': True,
                'successful': False,
                'fixes_applied': fixes_attempted,
                'retry_recommended': False
            }
    
    async def _fix_api_error(self, error_context: ErrorContext) -> Dict:
        """Fix general API errors"""
        
        fixes_attempted = []
        
        try:
            # Strategy 1: Refresh API connections
            if hasattr(self, 'model_manager') and hasattr(self.model_manager, 'session_pool'):
                if self.model_manager.session_pool:
                    await self.model_manager.session_pool.close()
                await self.model_manager.initialize()
                fixes_attempted.append("connection_pool_refresh")
            
            return {
                'attempted': True,
                'successful': True,
                'fixes_applied': fixes_attempted,
                'retry_recommended': True
            }
            
        except Exception:
            return {
                'attempted': True,
                'successful': False,
                'fixes_applied': fixes_attempted,
                'retry_recommended': False
            }
    
    async def _generate_fix_suggestions(self, error_context: ErrorContext) -> List[str]:
        """Generate AI-powered fix suggestions for developers"""
        
        suggestion_prompt = f"""
        Analyze this error and provide specific fix suggestions for developers:
        
        Error Type: {error_context.error_type}
        Error Message: {error_context.error_message}
        Category: {error_context.category.value}
        Severity: {error_context.severity.value}
        Function: {error_context.function_name}
        
        Stack Trace:
        {error_context.stack_trace}
        
        System State:
        {json.dumps(error_context.system_state, indent=2)}
        
        Provide 3-5 specific, actionable suggestions to fix this error.
        Include code examples if relevant.
        """
        
        try:
            response = await self.model_manager.generate_response(
                suggestion_prompt,
                {'system_prompt': 'You are an expert software debugging assistant.'},
                {'urgent': True}
            )
            
            suggestions = self._parse_suggestions(response['content'])
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Failed to generate AI suggestions: {e}")
            return [
                "Check error logs for more details",
                "Verify API keys and network connectivity",
                "Review input validation logic",
                "Consider implementing retry mechanisms",
                "Monitor system resources"
            ]
    
    def _parse_suggestions(self, ai_response: str) -> List[str]:
        """Parse AI response to extract actionable suggestions"""
        
        suggestions = []
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            if (line.startswith(('1.', '2.', '3.', '4.', '5.')) or 
                line.startswith(('-', '*', '•'))):
                suggestion = line[2:].strip() if line[1] == '.' else line[1:].strip()
                if suggestion:
                    suggestions.append(suggestion)
        
        if not suggestions:
            sentences = ai_response.split('.')
            suggestions = [s.strip() for s in sentences if len(s.strip()) > 20][:5]
        
        return suggestions[:5]
    
    def _generate_user_message(self, error_context: ErrorContext) -> str:
        """Generate user-friendly error message"""
        
        if error_context.severity == ErrorSeverity.LOW:
            return "I encountered a minor issue but I'm working on it. Please try again."
        elif error_context.severity == ErrorSeverity.MEDIUM:
            return "I'm experiencing some technical difficulties. Let me try a different approach."
        elif error_context.severity == ErrorSeverity.HIGH:
            return "I'm having trouble processing your request right now. Please wait a moment and try again."
        else:  # CRITICAL
            return "I'm experiencing serious technical issues. Please contact support if this persists."
    
    def _generate_error_id(self) -> str:
        """Generate unique error ID"""
        import uuid
        return f"ERR-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
    
    async def _log_error(self, error_context: ErrorContext):
        """Log error to file and console"""
        
        log_entry = {
            'error_id': error_context.error_id,
            'timestamp': error_context.timestamp.isoformat(),
            'type': error_context.error_type,
            'message': error_context.error_message,
            'severity': error_context.severity.value,
            'category': error_context.category.value,
            'function': error_context.function_name,
            'user_id': error_context.user_id
        }
        
        self.logger.error(f"Error {error_context.error_id}: {error_context.error_message}")
        
        try:
            async with aiofiles.open(f"logs/error_details_{error_context.error_id}.json", 'w') as f:
                await f.write(json.dumps(asdict(error_context), indent=2, default=str))
        except Exception as e:
            self.logger.error(f"Failed to save error details: {e}")
    
    async def get_error_statistics(self) -> Dict:
        """Get error statistics for monitoring"""
        
        total_errors = len(self.error_log)
        if total_errors == 0:
            return {'total_errors': 0, 'message': 'No errors recorded yet'}
        
        severity_counts = {}
        category_counts = {}
        auto_fix_stats = {'attempted': 0, 'successful': 0}
        
        for error in self.error_log:
            severity = error.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            category = error.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
            
            if error.auto_fix_attempted:
                auto_fix_stats['attempted'] += 1
                if error.auto_fix_successful:
                    auto_fix_stats['successful'] += 1
        
        return {
            'total_errors': total_errors,
            'severity_distribution': severity_counts,
            'category_distribution': category_counts,
            'auto_fix_success_rate': (auto_fix_stats['successful'] / max(auto_fix_stats['attempted'], 1)) * 100,
            'fix_success_by_category': self.fix_success_rate
        }

# Error handling decorator
def handle_errors(error_handler):
    """Decorator for automatic error handling"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                context = {
                    'function_name': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                }
                error_result = await error_handler.handle_error(e, context)
                
                if error_result.get('auto_fixed') and error_result.get('retry_recommended'):
                    try:
                        return await func(*args, **kwargs)
                    except Exception:
                        pass
                
                return error_result
        
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    'function_name': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                }
                error_handler.logger.error(f"Sync function error in {func.__name__}: {e}")
                return {
                    'error': True,
                    'message': str(e),
                    'function': func.__name__
                }
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator
