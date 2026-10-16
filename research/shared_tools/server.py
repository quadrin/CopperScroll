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
            elif parsed.path == '/kb':
                body = (HERE / 'claim_kb' / 'index.html').read_bytes()
                mime = 'text/html; charset=utf-8'
            elif parsed.path == '/kb/schema.svg':
                body = (HERE / 'claim_kb' / 'schema.svg').read_bytes()
                mime = 'image/svg+xml'
            else:
                if parsed.path.startswith('/api/kb/'):
                    from claim_kb import store
                    from claim_kb.model import public_view
                    from claim_kb.queries import Queries
                    if parsed.path == '/api/kb/changes':
                        result = store.changes()
                    else:
                        data, version = store.load()
                        data = public_view(data)
                        q = Queries(data)
                        route = parsed.path.removeprefix('/api/kb/')
                        identity = params.get('id', [''])[0]
                        if route == 'graph': result = data
                        elif route == 'entry': result = q.entry(identity or '60')
                        elif route == 'claim': result = q.evidence_chain(identity)
                        elif route == 'impact': result = q.impact(identity)
                        elif route == 'names': result = q.chronology()
                        elif route == 'locator':
                            from claim_kb.locators import resolve
                            from core import ROOT
                            result = resolve(data, ROOT, identity, int(params.get('n',['0'])[0]), version['base_commit'])
                        elif route == 'query':
                            number = int(params.get('number', ['1'])[0])
                            functions = {1:lambda:q.impact(identity or 'reading/e60-janoah:4'),
                                2:q.same_observation,3:lambda:q.candidate(identity or 'iv17'),
                                4:q.coexistence,5:q.no_external_match,
                                6:lambda:q.impact(identity or 'claim/relationships-quarries-later-phase'),
                                7:q.acquisition,8:q.uninspected}
                            if number not in functions: raise ValueError('Unknown query')
                            result = functions[number]()
                        else:
                            self.send_error(404)
                            return
                        result = {'version':version,'result':result}
                elif parsed.path == '/api/search':
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
