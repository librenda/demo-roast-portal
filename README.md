# Akatos Pitch Roast - Judge App

A web-based judging system for pitch competitions. Judges can submit scores and feedback, and view real-time results on a shared dashboard.

## Features

- 📝 **Judge Form**: Submit scores for 4 criteria (Narrative, Delivery, Idea, Problem/Market)
- 📊 **Dashboard**: View all submissions in real-time
- 🚫 **Red X System**: Judges can stop boring pitches (stops at 3 Xs)
- 💾 **Shared Storage**: All judges see the same data across different computers
- 📥 **CSV Export**: Export submissions and individual rubrics

## Setup

### 1. Install Dependencies

Make sure you have Python 3 installed, then:

```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows

# Install required packages
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python server.py
```

The server will start on `http://localhost:5000`

### 3. Access the App

- **Judge Form**: http://localhost:5000/ (or http://YOUR_IP:5000/)
- **Dashboard**: http://localhost:5000/dashboard (or http://YOUR_IP:5000/dashboard)

## Using on Multiple Computers

To allow judges on different computers to access the app:

1. **Find your IP address**:
   - **Mac/Linux**: Run `ifconfig` or `ip addr show` and look for your local IP (usually starts with 192.168.x.x or 10.x.x.x)
   - **Windows**: Run `ipconfig` and look for "IPv4 Address"

2. **Share the URL**: Other judges should visit:
   - `http://YOUR_IP:5000/` for the judge form
   - `http://YOUR_IP:5000/dashboard` for the dashboard

3. **Firewall**: Make sure your firewall allows connections on port 5000

## How It Works

- The server stores all submissions in `judge_data.json`
- Judges submit scores through the web form
- The dashboard automatically refreshes every 10 seconds
- Red X counts are shared across all judges in real-time
- If the server is unavailable, the app falls back to localStorage (but won't be shared)

## Data Storage

All data is stored in `judge_data.json` in the project directory. This file contains:
- All judge submissions
- Red X votes
- Timestamps

**Backup this file regularly!**

## Troubleshooting

- **Can't connect from other computers**: Check firewall settings and make sure you're using the correct IP address
- **Data not syncing**: Make sure the server is running and all judges are using the same server URL
- **Port already in use**: Change the port in `server.py` (line 133) from 5000 to another port like 5001

## Development

The app uses:
- **Backend**: Flask (Python)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Storage**: JSON file (can be easily migrated to a database)

