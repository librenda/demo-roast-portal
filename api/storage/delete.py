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
        
        if not key:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Key required'}).encode('utf-8'))
            return
        
        db = load_data()
        
        # Try to delete from submissions
        if key in db.get('submissions', {}):
            del db['submissions'][key]
            save_data(db)
        
        # Try to delete from red_xs
        if key in db.get('red_xs', {}):
            del db['red_xs'][key]
            save_data(db)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

