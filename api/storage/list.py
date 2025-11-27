from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

# Use Vercel KV REST API
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
        except Exception as e:
            print(f"KV load error: {e}")
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
        except Exception as e:
            print(f"KV save error: {e}")
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
        
        prefix = data.get('prefix', '')
        include_values = data.get('includeValues', False)
        
        db = load_data()
        submissions = db.get('submissions', {})
        red_xs = db.get('red_xs', {})
        
        keys = []
        items = []
        
        # Check submissions
        for key in submissions.keys():
            if not prefix or key.startswith(prefix):
                keys.append(key)
                if include_values:
                    items.append({
                        'key': key,
                        'value': json.dumps(submissions[key])
                    })
        
        # Check red Xs
        for key in red_xs.keys():
            if not prefix or key.startswith(prefix):
                if key not in keys:
                    keys.append(key)
                    if include_values:
                        items.append({
                            'key': key,
                            'value': red_xs[key]
                        })
        
        result = {'keys': keys}
        if include_values:
            result['items'] = items
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

