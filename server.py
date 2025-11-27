#!/usr/bin/env python3
"""
Akatos Pitch Roast - Backend Server
Simple Flask server to share judge submissions across multiple computers
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__, static_folder='.')
CORS(app)  # Allow cross-origin requests so judges on different computers can access

# Data file to store all submissions
DATA_FILE = 'judge_data.json'

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'submissions': {}, 'red_xs': {}}
    return {'submissions': {}, 'red_xs': {}}

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    """Serve the judge form"""
    return send_from_directory('.', 'judge-form.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard"""
    return send_from_directory('.', 'judge-dashboard.html')

@app.route('/api/storage/list', methods=['POST'])
def list_storage():
    """List all keys with optional prefix filtering"""
    data = request.get_json() or {}
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
    
    # Check red Xs (for pitch X tracking)
    for key in red_xs.keys():
        if not prefix or key.startswith(prefix):
            if key not in keys:  # Avoid duplicates
                keys.append(key)
                if include_values:
                    items.append({
                        'key': key,
                        'value': red_xs[key]
                    })
    
    result = {'keys': keys}
    if include_values:
        result['items'] = items
    
    return jsonify(result)

@app.route('/api/storage/get', methods=['POST'])
def get_storage():
    """Get a value by key"""
    data = request.get_json() or {}
    key = data.get('key')
    
    if not key:
        return jsonify({'error': 'Key required'}), 400
    
    db = load_data()
    submissions = db.get('submissions', {})
    
    if key in submissions:
        return jsonify({'value': json.dumps(submissions[key])})
    else:
        return jsonify({'value': None})

@app.route('/api/storage/set', methods=['POST'])
def set_storage():
    """Set a value by key"""
    data = request.get_json() or {}
    key = data.get('key')
    value = data.get('value')
    
    if not key or value is None:
        return jsonify({'error': 'Key and value required'}), 400
    
    db = load_data()
    
    # Handle submission storage
    if key.startswith('submission_'):
        try:
            submission_data = json.loads(value)
            db.setdefault('submissions', {})[key] = submission_data
            save_data(db)
            return jsonify({'success': True})
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON value'}), 400
    
    # Handle red X storage
    elif key.endswith('_x_') or '_x_' in key:
        db.setdefault('red_xs', {})[key] = value
        save_data(db)
        return jsonify({'success': True})
    
    # Generic storage
    else:
        db.setdefault('submissions', {})[key] = value
        save_data(db)
        return jsonify({'success': True})

@app.route('/api/storage/delete', methods=['POST'])
def delete_storage():
    """Delete a value by key"""
    data = request.get_json() or {}
    key = data.get('key')
    
    if not key:
        return jsonify({'error': 'Key required'}), 400
    
    db = load_data()
    
    # Try to delete from submissions
    if key in db.get('submissions', {}):
        del db['submissions'][key]
        save_data(db)
        return jsonify({'success': True})
    
    # Try to delete from red_xs
    if key in db.get('red_xs', {}):
        del db['red_xs'][key]
        save_data(db)
        return jsonify({'success': True})
    
    return jsonify({'success': True})  # Already deleted or doesn't exist

@app.route('/api/red-x/list', methods=['POST'])
def list_red_xs():
    """List all red Xs for a pitch"""
    data = request.get_json() or {}
    prefix = data.get('prefix', '')
    
    db = load_data()
    red_xs = db.get('red_xs', {})
    
    keys = []
    for key in red_xs.keys():
        if not prefix or key.startswith(prefix):
            keys.append(key)
    
    return jsonify({'keys': keys})

@app.route('/api/storage/list', methods=['GET'])
def list_storage_get():
    """List all keys - GET endpoint for easier testing"""
    prefix = request.args.get('prefix', '')
    include_values = request.args.get('includeValues', 'false').lower() == 'true'
    
    db = load_data()
    submissions = db.get('submissions', {})
    
    keys = []
    items = []
    
    for key in submissions.keys():
        if not prefix or key.startswith(prefix):
            keys.append(key)
            if include_values:
                items.append({
                    'key': key,
                    'value': json.dumps(submissions[key])
                })
    
    result = {'keys': keys}
    if include_values:
        result['items'] = items
    
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 Starting Akatos Pitch Roast Server...")
    print("📝 Judge Form: http://localhost:5000/")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("\n💡 To allow other computers to access:")
    print("   1. Find your IP address (ifconfig on Mac/Linux, ipconfig on Windows)")
    print("   2. Other judges should visit: http://YOUR_IP:5000/")
    print("\n⚠️  Make sure your firewall allows connections on port 5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

