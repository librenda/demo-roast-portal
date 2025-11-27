from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

KV_URL = os.environ.get('KV_REST_API_URL')
KV_TOKEN = os.environ.get('KV_REST_API_TOKEN')

def load_data():
    """Load data from Vercel KV or return empty dict"""
    if KV_URL and KV_TOKEN:
        try:
            req = urllib.request.Request(f"{KV_URL}/get/judge_data")
            req.add_header('Authorization', f'Bearer {KV_TOKEN}')
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                if result.get('result'):
                    return json.loads(result['result'])
        except:
            return {'submissions': {}, 'red_xs': {}}
    return {'submissions': {}, 'red_xs': {}}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
        except:
            data = {}
        
        key = data.get('key')
        
        if not key:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Key required'}).encode('utf-8'))
            return
        
        db = load_data()
        submissions = db.get('submissions', {})
        
        if key in submissions:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'value': json.dumps(submissions[key])}).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'value': None}).encode('utf-8'))

