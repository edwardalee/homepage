#!/usr/bin/env python3
"""
Simple HTTP server with Server Side Includes (SSI) support.
Usage: python serve.py [port]
Default port is 8000.

This server handles /~eal/ path rewriting for local preview of the
ptolemy.berkeley.edu/~eal/ website.
"""

import http.server
import socketserver
import os
import re
import sys

class SSIHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with SSI support and path rewriting."""
    
    def translate_path(self, path):
        """Translate URL path to filesystem path, handling /~eal/ prefix."""
        # Strip /~eal prefix if present
        if path.startswith('/~eal/'):
            path = path[5:]  # Keep the leading /
        elif path == '/~eal':
            path = '/'
        
        return super().translate_path(path)
    
    def do_GET(self):
        # Get the file path (translate_path handles /~eal/ rewriting)
        path = self.translate_path(self.path)
        
        # Only process HTML files for SSI
        if os.path.isfile(path) and path.endswith(('.html', '.htm', '.shtml')):
            try:
                content = self.process_ssi(path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self.send_error(500, f"SSI processing error: {e}")
                return
        
        # For non-HTML files, use default handler
        super().do_GET()
    
    def process_ssi(self, filepath):
        """Process SSI directives in a file."""
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Get the directory of the current file for relative includes
        base_dir = os.path.dirname(filepath)
        doc_root = os.getcwd()
        
        # Process <!--#include virtual="..." --> directives
        pattern = r'<!--\s*#include\s+virtual\s*=\s*"([^"]+)"\s*-->'
        
        def replace_include(match):
            include_path = match.group(1)
            
            # Strip /~eal/ prefix if present (for local preview)
            if include_path.startswith('/~eal/'):
                include_path = include_path[5:]  # Keep leading /
            
            # Handle virtual paths (relative to document root or current file)
            if include_path.startswith('/'):
                # Absolute path from document root
                full_path = os.path.join(doc_root, include_path.lstrip('/'))
            else:
                # Relative path from current file
                full_path = os.path.normpath(os.path.join(base_dir, include_path))
            
            if os.path.isfile(full_path):
                # Recursively process included files for nested SSI
                return self.process_ssi(full_path).decode('utf-8')
            else:
                print(f"  Warning: SSI include not found: {include_path} -> {full_path}")
                return f'<!-- SSI include not found: {include_path} -->'
        
        processed = re.sub(pattern, replace_include, content)
        return processed.encode('utf-8')
    
    def log_message(self, format, *args):
        """Log with color coding for errors."""
        message = format % args
        if '404' in message or '500' in message:
            # Red for errors
            print(f"\033[91m{self.address_string()} - {message}\033[0m")
        else:
            print(f"{self.address_string()} - {message}")

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    
    # Allow socket reuse to avoid "Address already in use" errors
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", port), SSIHandler) as httpd:
        print(f"Serving at http://localhost:{port}/")
        print(f"For full site preview: http://localhost:{port}/~eal/index.html")
        print("Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()
