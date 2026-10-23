# -*- coding: utf-8 -*-
import os
import time
import threading
from datetime import datetime
from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

STREAMLIT_URL = "https://shahajjo.streamlit.app/"

last_ping_time = "Ekhono kono ping hoyni"
next_ping_timestamp = 0
last_status_code = "Waiting..."
last_error_message = "Kono error nei (Bot active ache)"

def keep_alive_background_ping():
    global last_ping_time, next_ping_timestamp, last_status_code, last_error_message
    while True:
        try:
            print("🌐 Sending HTTP GET request to Streamlit...")
            response = requests.get(STREAMLIT_URL, timeout=30)
            last_status_code = str(response.status_code)
            last_ping_time = datetime.now().strftime("%I:%M:%S %p (%d %b)")
            last_error_message = f"Success (HTTP Status: {response.status_code})"
            print(f"✅ Ping successful at {last_ping_time} with status {response.status_code}")
        except Exception as e:
            last_error_message = str(e)
            last_status_code = "Error"
            print(f"⚠️ Ping error: {e}")
        
        # Prottee 1 minute (60 seconds) por por ping korbe
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
            .error-card {
                background: #fff5f5;
                border-left: 4px solid #e53e3e;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                font-size: 13px;
                text-align: left;
                color: #c53030;
                word-break: break-all;
            }
            .screenshot-box {
                border: 2px dashed #cbd5e1;
                border-radius: 10px;
                padding: 12px;
                background: #fafafa;
            }
            .screenshot-box h3 {
                margin-top: 0;
                color: #4a5568;
                font-size: 16px;
            }
            img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                border: 1px solid #e2e8f0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Shahajjo AI Keeper Dashboard</h1>
            <div class="subtitle">Pure Python 1-Min Ping & 5-Sec Preview Updater</div>
            <div class="status-badge">🟢 Bot Active & Running 24/7</div>
            
            <div class="info-card">
                🕒 <strong>Last Ping Time:</strong> <span id="last-time">{{ last_time }}</span><br>
                🌐 <strong>Streamlit Status:</strong> <span id="status-code">{{ status_code }}</span>
            </div>

            <div class="timer-card">
                ⏳ <strong>Next Ping In:</strong> <span id="countdown">Calculating...</span>
            </div>

            <div class="error-card">
                ⚠️ <strong>Status Log:</strong> <span id="error-log">{{ error_msg }}</span>
            </div>
            
            <div class="screenshot-box">
                <h3>📷 Live Streamlit App Preview (Refreshes Every 5s):</h3>
                <div id="image-container">
                    <img id="live-ss" src="https://s0.wordpress.com/mshots/v1/https://shahajjo.streamlit.app/?w=1280&h=800" alt="Streamlit Live Preview">
                </div>
            </div>
        </div>

        <script>
            var targetTime = {{ next_time }};
            
            function updateTimer() {
                if (targetTime === 0) {
                    document.getElementById("countdown").innerText = "Prothom ping processing-e ache...";
                    return;
                }
                
                var now = Math.floor(Date.now() / 1000);
                var secondsLeft = targetTime - now;
                
                if (secondsLeft <= 0) {
                    document.getElementById("countdown").innerText = "Ping hocche...";
                } else {
                    var mins = Math.floor(secondsLeft / 60);
                    var secs = secondsLeft % 60;
                    document.getElementById("countdown").innerText = mins + "m " + (secs < 10 ? "0" : "") + secs + "s";
                }
            }
            
            setInterval(updateTimer, 1000);
            updateTimer();

            // Prottee 5 second por por background fetch kore preview update korbe
            function autoRefreshData() {
                fetch('/status-json')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("last-time").innerText = data.last_time;
                        document.getElementById("status-code").innerText = data.status_code;
                        document.getElementById("error-log").innerText = data.error_msg;
                        targetTime = data.next_time;
                        
                        var imgElem = document.getElementById("live-ss");
                        if (imgElem) {
                            imgElem.src = "https://s0.wordpress.com/mshots/v1/https://shahajjo.streamlit.app/?w=1280&h=800&t=" + Date.now();
                        }
                    })
                    .catch(err => console.log('Fetch error:', err));
            }

            setInterval(autoRefreshData, 5000); // 5 seconds interval
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
        timestamp=timestamp
    )

@app.route("/status-json")
def status_json():
    return jsonify({
        "last_time": last_ping_time,
        "next_time": int(next_ping_timestamp),
        "status_code": last_status_code,
        "error_msg": last_error_message
    })

if __name__ == "__main__":
    next_ping_timestamp = time.time() + 60
    t = threading.Thread(target=keep_alive_background_ping)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)