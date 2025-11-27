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

def save_data(data):
    """Save data to Vercel KV"""
    if KV_URL and KV_TOKEN:
        try:
            data_json = json.dumps(data)
            req = urllib.request.Request(
                f"{KV_URL}/set/judge_data",
                data=json.dumps({'value': data_json}).encode('utf-8'),
                headers={'Authorization': f'Bearer {KV_TOKEN}', 'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req)
            return True
        except:
            return False
    return False

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
        except:
            data = {}
        
        key = data.get('key')
        value = data.get('value')
        
        if not key or value is None:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Key and value required'}).encode('utf-8'))
            return
        
        db = load_data()
        
        # Handle submission storage
        if key.startswith('submission_'):
            try:
                submission_data = json.loads(value)
                db.setdefault('submissions', {})[key] = submission_data
                save_data(db)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid JSON value'}).encode('utf-8'))
        
        # Handle red X storage
        elif key.endswith('_x_') or '_x_' in key:
            db.setdefault('red_xs', {})[key] = value
            save_data(db)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        
        # Generic storage
        else:
            db.setdefault('submissions', {})[key] = value
            save_data(db)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

