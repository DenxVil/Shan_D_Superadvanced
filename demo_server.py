#!/usr/bin/env python3
"""
Simple demonstration server for Shan-D website
Shows that the website loads correctly
"""

import http.server
import socketserver
import os
from pathlib import Path

# Change to static directory
static_dir = Path(__file__).parent / "static"
os.chdir(static_dir)

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

print(f"🌐 Starting Shan-D website demo server on http://localhost:{PORT}")
print(f"📁 Serving files from: {static_dir}")
print("🚀 Website should be accessible and fully functional!")
print("\n📋 Available endpoints:")
print(f"   http://localhost:{PORT}/         - Main website")
print(f"   http://localhost:{PORT}/index.html - Direct HTML file")

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")