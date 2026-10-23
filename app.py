# -*- coding: utf-8 -*-
import os
import time
import threading
from datetime import datetime
from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

STREAMLIT_URL = "https://shahajjo.streamlit.app/"

last_ping_time = "Waiting for first ping..."
next_ping_timestamp = 0
last_status_code = "Waiting..."
last_error_message = "Initializing bot..."
is_success = True

def keep_alive_background_ping():
    global last_ping_time, next_ping_timestamp, last_status_code, last_error_message, is_success
    while True:
        try:
            print("🌐 Sending HTTP GET request to Streamlit...")
            response = requests.get(STREAMLIT_URL, timeout=30)
            last_status_code = str(response.status_code)
            last_ping_time = datetime.now().strftime("%I:%M:%S %p (%d %b)")
            if response.status_code == 200:
                last_error_message = f"Success: HTTP Status {response.status_code} OK"
                is_success = True
            else:
                last_error_message = f"Warning: HTTP Status {response.status_code}"
                is_success = False
            print(f"✅ Ping successful at {last_ping_time} with status {response.status_code}")
        except Exception as e:
            last_error_message = f"Error: {str(e)}"
            last_status_code = "Failed"
            is_success = False
            print(f"⚠️ Ping error: {e}")
        
        # Next ping in 1 minute (60 seconds)
        next_ping_timestamp = time.time() + 60
        print("💤 Waiting 1 minute for next ping cycle...")
        time.sleep(60)

@app.route("/")
def home():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shahajjo AI Keeper Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f0f2f5;
                margin: 0;
                padding: 15px;
                color: #333;
                text-align: center;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            }
            h1 {
                color: #1a202c;
                font-size: 24px;
                margin-bottom: 5px;
            }
            .subtitle {
                color: #718096;
                font-size: 13px;
                margin-bottom: 15px;
            }
            .status-badge {
                display: inline-block;
                background-color: #27ae60;
                color: white;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .info-card {
                background: #ebf8ff;
                border-left: 4px solid #3182ce;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 15px;
                font-size: 14px;
                text-align: left;
                color: #2b6cb0;
            }
            .timer-card {
                background: #fefcbf;
                border-left: 4px solid #d69e2e;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 15px;
                font-size: 15px;
                font-weight: bold;
                color: #744210;
                text-align: left;
            }
            .status-card-success {
                background: #f0fff4;
                border-left: 4px solid #38a169;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                font-size: 13px;
                text-align: left;
                color: #276749;
                word-break: break-all;
                font-weight: 500;
            }
            .status-card-error {
                background: #fff5f5;
                border-left: 4px solid #e53e3e;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                font-size: 13px;
                text-align: left;
                color: #c53030;
                word-break: break-all;
                font-weight: 500;
            }
            .action-box {
                border: 2px dashed #cbd5e1;
                border-radius: 10px;
                padding: 20px;
                background: #fafafa;
            }
            .action-box h3 {
                margin-top: 0;
                color: #4a5568;
                font-size: 16px;
            }
            .visit-btn {
                background-color: #3182ce;
                color: white;
                border: none;
                padding: 12px 25px;
                font-size: 15px;
                font-weight: bold;
                border-radius: 6px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                transition: background 0.2s;
            }
            .visit-btn:hover {
                background-color: #2b6cb0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Shahajjo AI Keeper Dashboard</h1>
            <div class="subtitle">Pure Python 1-Minute Ping & Uptime Monitor</div>
            <div class="status-badge">🟢 Bot Active & Running 24/7</div>
            
            <div class="info-card">
                🕒 <strong>Last Ping Time:</strong> <span id="last-time">{{ last_time }}</span><br>
                🌐 <strong>Streamlit Status:</strong> <span id="status-code">{{ status_code }}</span>
            </div>

            <div class="timer-card">
                ⏳ <strong>Next Ping In:</strong> <span id="countdown">Calculating...</span>
            </div>

            <div id="log-card" class="{% if is_success %}status-card-success{% else %}status-card-error{% endif %}">
                📌 <strong>Status Log:</strong> <span id="error-log">{{ error_msg }}</span>
            </div>
            
            <div class="action-box">
                <h3>🔗 Live Streamlit App Access:</h3>
                <p style="font-size: 13px; color: #718096; margin-bottom: 15px;">Click below to open your active Streamlit app directly in a new tab:</p>
                <a href="https://shahajjo.streamlit.app/" target="_blank" class="visit-btn">🌐 Open Shahajjo App</a>
            </div>
        </div>

        <script>
            var targetTime = {{ next_time }};
            
            function updateTimer() {
                if (targetTime === 0) {
                    document.getElementById("countdown").innerText = "Initializing first ping...";
                    return;
                }
                
                var now = Math.floor(Date.now() / 1000);
                var secondsLeft = targetTime - now;
                
                if (secondsLeft <= 0) {
                    document.getElementById("countdown").innerText = "Pinging now...";
                } else {
                    var mins = Math.floor(secondsLeft / 60);
                    var secs = secondsLeft % 60;
                    document.getElementById("countdown").innerText = mins + "m " + (secs < 10 ? "0" : "") + secs + "s";
                }
            }
            
            setInterval(updateTimer, 1000);
            updateTimer();

            function autoRefreshData() {
                fetch('/status-json')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("last-time").innerText = data.last_time;
                        document.getElementById("status-code").innerText = data.status_code;
                        document.getElementById("error-log").innerText = data.error_msg;
                        targetTime = data.next_time;
                        
                        var logCard = document.getElementById("log-card");
                        if (data.is_success) {
                            logCard.className = "status-card-success";
                        } else {
                            logCard.className = "status-card-error";
                        }
                    })
                    .catch(err => console.log('Fetch error:', err));
            }

            setInterval(autoRefreshData, 5000);
        </script>
    </body>
    </html>
    """
    timestamp = time.time()
    return render_template_string(
        html_template, 
        last_time=last_ping_time, 
        next_time=int(next_ping_timestamp),
        status_code=last_status_code,
        error_msg=last_error_message,
        is_success=is_success,
        timestamp=timestamp
    )

@app.route("/status-json")
def status_json():
    return jsonify({
        "last_time": last_ping_time,
        "next_time": int(next_ping_timestamp),
        "status_code": last_status_code,
        "error_msg": last_error_message,
        "is_success": is_success
    })

if __name__ == "__main__":
    next_ping_timestamp = time.time() + 60
    t = threading.Thread(target=keep_alive_background_ping)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)