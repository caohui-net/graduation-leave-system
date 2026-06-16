#!/usr/bin/env python3
"""
前端静态文件服务器 - 带Cache-Control配置
用途：替代python -m http.server，防止HTML缓存问题
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer as HTTPServer
import os
import sys

class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
    """自定义Handler，为HTML文件禁用缓存"""

    def end_headers(self):
        # HTML文件禁止缓存
        if self.path.endswith('.html') or self.path == '/':
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        # JS/CSS文件长期缓存（依赖URL版本号）
        elif self.path.endswith('.js') or self.path.endswith('.css'):
            self.send_header('Cache-Control', 'public, max-age=31536000')
        # 其他静态资源短期缓存
        else:
            self.send_header('Cache-Control', 'public, max-age=86400')

        SimpleHTTPRequestHandler.end_headers(self)

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7788
    directory = sys.argv[2] if len(sys.argv) > 2 else 'demo-web'

    os.chdir(directory)

    server = HTTPServer(('0.0.0.0', port), NoCacheHTTPRequestHandler)
    print(f'✓ Serving at http://0.0.0.0:{port}')
    print(f'  Directory: {os.getcwd()}')
    print(f'  Cache-Control: HTML=no-cache, JS/CSS=1year')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n✓ Server stopped')

if __name__ == '__main__':
    main()
