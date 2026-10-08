"""Read-only local UI. No network fetches, credential handling or mutations."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import json
from core import HERE, cached_dataset, search, image_query
from benchmarks import run


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        try:
            if parsed.path == '/':
                body = (HERE / 'index.html').read_bytes()
                mime = 'text/html; charset=utf-8'
            else:
                if parsed.path == '/api/search':
                    result = search(params.get('q', [''])[0], params.get('kind', [None])[0], 30)
                elif parsed.path == '/api/map':
                    result = image_query(cached_dataset('manuscript'),
                                         line=params.get('line', [None])[0],
                                         cut=int(params['cut'][0]) if params.get('cut') else None,
                                         column=int(params['column'][0]) if params.get('column') else None,
                                         substrate=params.get('substrate', [None])[0])
                elif parsed.path == '/api/entries':
                    result = cached_dataset('entries')
                elif parsed.path == '/api/controls':
                    result = cached_dataset('controls')
                elif parsed.path == '/api/benchmark':
                    result = run()
                else:
                    self.send_error(404)
                    return
                body = json.dumps(result, ensure_ascii=False, allow_nan=False).encode()
                mime = 'application/json; charset=utf-8'
            self.send_response(200)
        except (ValueError, FileNotFoundError) as error:
            body = json.dumps({'error': str(error)}).encode()
            mime = 'application/json'
            self.send_response(400)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def serve(port=8765):
    print(f'Local research tools: http://127.0.0.1:{port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
