#!/usr/bin/env python3
"""
Denvil 😏
Web Application Module for Shan_D_Superadvanced
Integrates with existing Telegram bot functionality
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from aiohttp import web, WSMsgType
from aiohttp_cors import setup as cors_setup, ResourceOptions
import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from ..core.model_manager import AdvancedModelManager
from ..core.reasoning_engine import AdvancedReasoningEngine
from ..core.multimodal_processor import MultimodalProcessor
from ..bot.telegram_bot import ShanDAdvanced
from ..utils.config import load_config
from ..utils.certificate_generator import certificate_generator
from ..utils.mail_config import mail_config
from ..storage.certificate_db import certificate_db

class ShanDWebApp:
    """Web application wrapper for Shan_D_Superadvanced"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.app = None
        self.shan_d_bot = None
        self.model_manager = None
        self.reasoning_engine = None
        self.multimodal_processor = None
        self.websocket_connections = set()
        
    async def initialize(self):
        """Initialize all components"""
        try:
            # Initialize core components
            self.model_manager = AdvancedModelManager(self.config)
            self.reasoning_engine = AdvancedReasoningEngine(self.config)
            self.multimodal_processor = MultimodalProcessor(self.config)
            
            # Initialize Telegram bot (optional, for dual mode)
            self.shan_d_bot = ShanDAdvanced(self.config)
            await self.shan_d_bot.initialize()
            
            # Create web application
            self.app = await self._create_app()
            
            self.logger.info("✅ Shan_D_Superadvanced web application initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize web application: {str(e)}")
            raise
    
    async def _create_app(self) -> web.Application:
        """Create and configure aiohttp application"""
        
        # Create application with middleware
        app = web.Application(middlewares=[
            self._error_middleware,
            self._cors_middleware,
            self._logging_middleware
        ])
        
        # Setup session storage
        secret_key = self.config.get('web', {}).get('secret_key', 'your-secret-key-change-this')
        aiohttp_session.setup(app, EncryptedCookieStorage(secret_key.encode()))
        
        # Setup CORS
        cors = cors_setup(app, defaults={
            "*": ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        # Add routes
        self._setup_routes(app, cors)
        
        # Setup static files
        static_dir = Path(__file__).parent / "static"
        if static_dir.exists():
            app.router.add_static('/', static_dir, name='static')
        
        return app
    
    def _setup_routes(self, app: web.Application, cors):
        """Setup all application routes"""
        
        # API Routes
        api_routes = [
            ('GET', '/', self.index_handler),
            ('GET', '/health', self.health_handler),
            ('GET', '/api/status', self.api_status_handler),
            ('POST', '/api/chat', self.chat_handler),
            ('POST', '/api/analyze', self.analyze_handler),
            ('GET', '/api/models', self.models_handler),
            ('WebSocket', '/ws', self.websocket_handler),
            ('POST', '/api/certificate/generate', self.generate_certificate_handler),
            ('GET', '/api/certificate/status/{cert_id}', self.certificate_status_handler),
            ('GET', '/api/system/status', self.system_status_handler),
            ('GET', '/certificate/waiting', self.waiting_page_handler),
            ('GET', '/system/status', self.status_page_handler),
        ]
        
        for method, path, handler in api_routes:
            if method == 'WebSocket':
                app.router.add_get(path, handler)
            else:
                route = app.router.add_route(method, path, handler)
                cors.add(route)
    
    # Middleware
    async def _error_middleware(self, app, handler):
        """Global error handling middleware"""
        async def middleware_handler(request):
            try:
                return await handler(request)
            except web.HTTPException as ex:
                return web.json_response({
                    'error': str(ex),
                    'status': ex.status
                }, status=ex.status)
            except Exception as e:
                self.logger.error(f"Unhandled error: {str(e)}")
                return web.json_response({
                    'error': 'Internal server error',
                    'status': 500
                }, status=500)
        return middleware_handler
    
    async def _cors_middleware(self, app, handler):
        """CORS middleware"""
        async def middleware_handler(request):
            response = await handler(request)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        return middleware_handler
    
    async def _logging_middleware(self, app, handler):
        """Request logging middleware"""
        async def middleware_handler(request):
            start_time = datetime.utcnow()
            response = await handler(request)
            process_time = (datetime.utcnow() - start_time).total_seconds()
            
            self.logger.info(
                f"{request.method} {request.path} - "
                f"Status: {response.status} - "
                f"Time: {process_time:.3f}s"
            )
            return response
        return middleware_handler
    
    # Route Handlers
    async def index_handler(self, request):
        """Root endpoint with API documentation"""
        return web.json_response({
            "service": "Shan_D_Superadvanced",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "/": "API documentation",
                "/health": "Health check",
                "/api/status": "Service status",
                "/api/chat": "Chat with AI (POST)",
                "/api/analyze": "Analyze content (POST)",
                "/api/models": "Available models",
                "/ws": "WebSocket connection"
            },
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def health_handler(self, request):
        """Health check endpoint"""
        return web.json_response({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "model_manager": "online" if self.model_manager else "offline",
                "reasoning_engine": "online" if self.reasoning_engine else "offline",
                "multimodal_processor": "online" if self.multimodal_processor else "offline",
                "telegram_bot": "online" if self.shan_d_bot else "offline"
            }
        })
    
    async def api_status_handler(self, request):
        """Detailed API status"""
        return web.json_response({
            "service": "Shan_D_Superadvanced",
            "status": "operational",
            "uptime": "00:00:00",  # Implement actual uptime tracking
            "version": "1.0.0",
            "features": [
                "Chat AI",
                "Content Analysis",
                "Multimodal Processing",
                "Advanced Reasoning",
                "Telegram Integration"
            ]
        })
    
    async def chat_handler(self, request):
        """Handle chat requests"""
        try:
            data = await request.json()
            message = data.get('message', '')
            user_id = data.get('user_id', 'web_user')
            
            if not message:
                return web.json_response({
                    'error': 'Message is required'
                }, status=400)
            
            # Process message through reasoning engine
            if self.reasoning_engine:
                response = await self.reasoning_engine.process_query(
                    query=message,
                    user_id=user_id,
                    context=data.get('context', {})
                )
            else:
                response = {
                    'response': f"Echo: {message}",
                    'confidence': 1.0,
                    'processing_time': 0.1
                }
            
            return web.json_response({
                'response': response.get('response', 'No response generated'),
                'confidence': response.get('confidence', 0.0),
                'processing_time': response.get('processing_time', 0.0),
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"Chat handler error: {str(e)}")
            return web.json_response({
                'error': 'Failed to process chat message'
            }, status=500)
    
    async def analyze_handler(self, request):
        """Handle content analysis requests"""
        try:
            data = await request.json()
            content = data.get('content', '')
            analysis_type = data.get('type', 'general')
            
            if not content:
                return web.json_response({
                    'error': 'Content is required'
                }, status=400)
            
            # Use multimodal processor if available
            if self.multimodal_processor:
                result = await self.multimodal_processor.analyze_content(
                    content=content,
                    analysis_type=analysis_type
                )
            else:
                result = {
                    'analysis': f"Basic analysis of content: {len(content)} characters",
                    'type': analysis_type,
                    'confidence': 0.5
                }
            
            return web.json_response({
                'analysis': result,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"Analysis handler error: {str(e)}")
            return web.json_response({
                'error': 'Failed to analyze content'
            }, status=500)
    
    async def models_handler(self, request):
        """Get available models"""
        if self.model_manager:
            models = await self.model_manager.get_available_models()
        else:
            models = ['default']
        
        return web.json_response({
            'models': models,
            'default': models[0] if models else None,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    async def websocket_handler(self, request):
        """WebSocket handler for real-time communication"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.websocket_connections.add(ws)
        self.logger.info("New WebSocket connection established")
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        response = await self._handle_websocket_message(data)
                        await ws.send_str(json.dumps(response))
                    except json.JSONDecodeError:
                        await ws.send_str(json.dumps({
                            'error': 'Invalid JSON format'
                        }))
                elif msg.type == WSMsgType.ERROR:
                    self.logger.error(f'WebSocket error: {ws.exception()}')
        
        except Exception as e:
            self.logger.error(f"WebSocket handler error: {str(e)}")
        
        finally:
            self.websocket_connections.discard(ws)
            self.logger.info("WebSocket connection closed")
        
        return ws
    
    async def _handle_websocket_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming WebSocket messages"""
        message_type = data.get('type', 'chat')
        
        if message_type == 'chat':
            message = data.get('message', '')
            if self.reasoning_engine:
                response = await self.reasoning_engine.process_query(
                    query=message,
                    user_id=data.get('user_id', 'ws_user'),
                    context=data.get('context', {})
                )
            else:
                response = {'response': f"WebSocket echo: {message}"}
            
            return {
                'type': 'chat_response',
                'data': response,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        elif message_type == 'ping':
            return {'type': 'pong', 'timestamp': datetime.utcnow().isoformat()}
        
        else:
            return {'type': 'error', 'message': 'Unknown message type'}
    
    async def generate_certificate_handler(self, request):
        """Handle certificate generation requests"""
        try:
            data = await request.json()
            
            # Extract certificate data
            cert_data = {
                'certificate_id': data.get('certificate_id', f"CERT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),
                'user_name': data.get('name', ''),
                'course_name': data.get('course', ''),
                'issue_date': data.get('date', datetime.utcnow().strftime('%Y-%m-%d')),
                'email': data.get('email', '')
            }
            
            # Create database record
            try:
                certificate_db.create_certificate_record(cert_data)
            except Exception as db_error:
                self.logger.error(f"Database error: {db_error}")
                # Continue even if record creation fails
            
            # Generate certificate
            try:
                cert_path = certificate_generator.generate_certificate({
                    'certificate_id': cert_data['certificate_id'],
                    'name': cert_data['user_name'],
                    'course': cert_data['course_name'],
                    'date': cert_data['issue_date']
                })
                
                # Log successful attempt
                certificate_db.log_attempt(cert_data['certificate_id'], 'success')
                
                # Compare with template
                comparison = certificate_generator.compare_with_template(cert_path)
                
                # Update file path in database
                certificate_db.update_certificate_path(cert_data['certificate_id'], str(cert_path))
                
                # Send email if configured and email provided
                email_result = None
                if cert_data['email'] and mail_config.is_configured():
                    email_result = mail_config.send_certificate(
                        cert_data['email'],
                        cert_path,
                        cert_data['user_name'],
                        cert_data['certificate_id']
                    )
                
                return web.json_response({
                    'success': True,
                    'certificate_id': cert_data['certificate_id'],
                    'file_path': str(cert_path),
                    'comparison': comparison,
                    'email_sent': email_result.get('success', False) if email_result else False
                })
                
            except Exception as gen_error:
                # Log failed attempt
                certificate_db.log_attempt(
                    cert_data['certificate_id'],
                    'failed',
                    str(gen_error)
                )
                raise gen_error
            
        except Exception as e:
            self.logger.error(f"Certificate generation error: {e}")
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def certificate_status_handler(self, request):
        """Get certificate generation status"""
        cert_id = request.match_info['cert_id']
        
        try:
            cert_info = certificate_db.get_certificate(cert_id)
            
            if not cert_info:
                return web.json_response({
                    'error': 'Certificate not found'
                }, status=404)
            
            return web.json_response({
                'certificate_id': cert_id,
                'status': cert_info['status'],
                'attempts': cert_info['attempts'],
                'created_at': cert_info['created_at'],
                'updated_at': cert_info['updated_at']
            })
            
        except Exception as e:
            self.logger.error(f"Error fetching certificate status: {e}")
            return web.json_response({
                'error': str(e)
            }, status=500)
    
    async def system_status_handler(self, request):
        """Get comprehensive system status"""
        try:
            # Get mail configuration status
            mail_status = mail_config.get_status()
            
            # Get certificate system status
            template_exists = certificate_generator.template_path.exists()
            
            # Get database status
            db_connected = True
            tables_count = 2  # certificates and certificate_attempts
            try:
                conn = certificate_db.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM certificates")
                total_certs = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM certificates WHERE status='success'")
                success_certs = cursor.fetchone()[0]
                conn.close()
                
                success_rate = (success_certs / total_certs * 100) if total_certs > 0 else 0
            except Exception as db_error:
                self.logger.error(f"Database query error: {db_error}")
                db_connected = False
                total_certs = 0
                success_rate = 0
            
            # Get bot status
            bot_running = self.shan_d_bot is not None
            model_status = "online" if self.model_manager else "offline"
            
            return web.json_response({
                'mail': mail_status,
                'certificate': {
                    'template_exists': template_exists,
                    'total_generated': total_certs,
                    'success_rate': round(success_rate, 2)
                },
                'database': {
                    'connected': db_connected,
                    'tables_count': tables_count,
                    'schema_version': '1.0'
                },
                'bot': {
                    'running': bot_running,
                    'telegram': 'online' if bot_running else 'offline',
                    'model_manager': model_status,
                    'uptime': '00:00:00'  # TODO: Implement actual uptime tracking
                },
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"System status error: {e}")
            return web.json_response({
                'error': str(e)
            }, status=500)
    
    async def waiting_page_handler(self, request):
        """Serve the waiting page"""
        static_dir = Path(__file__).parent.parent / "static"
        waiting_page = static_dir / "waiting.html"
        
        if waiting_page.exists():
            return web.FileResponse(waiting_page)
        else:
            return web.json_response({
                'error': 'Waiting page not found'
            }, status=404)
    
    async def status_page_handler(self, request):
        """Serve the system status page"""
        static_dir = Path(__file__).parent.parent / "static"
        status_page = static_dir / "status.html"
        
        if status_page.exists():
            return web.FileResponse(status_page)
        else:
            return web.json_response({
                'error': 'Status page not found'
            }, status=404)


async def create_web_app(config: Dict[str, Any]) -> web.Application:
    """Factory function to create web application"""
    web_app = ShanDWebApp(config)
    await web_app.initialize()
    return web_app.app

# For direct testing
if __name__ == '__main__':
    async def main():
        config = load_config()
        app = await create_web_app(config)
        web.run_app(app, host='0.0.0.0', port=8080)
    
    asyncio.run(main())
