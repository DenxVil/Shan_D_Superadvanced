#!/usr/bin/env python3
"""
Simple web server for testing Shan_D_Superadvanced locally
Serves static files and handles API endpoints
"""

import asyncio
import json
import os
from pathlib import Path
from aiohttp import web, web_request
import aiohttp_cors
import sys

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import chat handler
from api.chat import process_chat_message

async def static_handler(request):
    """Serve static files"""
    path = request.match_info.get('path', 'index.html')
    
    if path == '':
        path = 'index.html'
    
    static_file = project_root / 'static' / path
    
    if static_file.exists() and static_file.is_file():
        return web.FileResponse(static_file)
    
    # Default to index.html for SPA routing
    index_file = project_root / 'static' / 'index.html'
    if index_file.exists():
        return web.FileResponse(index_file)
    
    return web.Response(text="File not found", status=404)

async def chat_api_handler(request):
    """Handle /api/chat requests"""
    
    if request.method == 'OPTIONS':
        return web.Response(
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        )
    
    if request.method != 'POST':
        return web.json_response({'error': 'Method not allowed'}, status=405)
    
    try:
        data = await request.json()
        message = data.get('message', '').strip()
        user_id = data.get('user_id', 'web_user')
        
        if not message:
            return web.json_response({'error': 'Message is required'}, status=400)
        
        result = await process_chat_message(message, user_id)
        return web.json_response(result)
        
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"API Error: {e}")
        return web.json_response({'error': 'Internal server error'}, status=500)

async def health_handler(request):
    """Health check endpoint"""
    return web.json_response({
        'status': 'healthy',
        'service': 'Shan_D_Superadvanced',
        'version': '1.0.0'
    })

async def create_app():
    """Create and configure the web application"""
    app = web.Application()
    
    # Setup CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Add routes
    chat_route = app.router.add_route('POST', '/api/chat', chat_api_handler)
    health_route = app.router.add_route('GET', '/health', health_handler)
    root_route = app.router.add_route('GET', '/', static_handler)
    static_route = app.router.add_route('GET', '/{path:.*}', static_handler)
    
    # Add CORS to specific routes (not OPTIONS routes)
    cors.add(chat_route)
    cors.add(health_route)
    cors.add(root_route)
    cors.add(static_route)
    
    return app

async def main():
    """Main function to run the server"""
    app = await create_app()
    
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting Shan_D_Superadvanced web server on port {port}")
    print(f"Access the application at: http://localhost:{port}")
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print("Server is running... Press Ctrl+C to stop")
    
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        pass
    finally:
        await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())