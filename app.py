# -*- coding: utf-8 -*-
import os
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, send_file, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Target Streamlit App
STREAMLIT_URL = "https://shahajjo.streamlit.app/"
SCREENSHOT_PATH = "latest_status.png"

# Global tracking variables
last_ping_time = "Ekhono kono session complete hoyni"
next_ping_timestamp = 0  # Epoch timestamp for JavaScript timer

def bot_scroll_and_keep_alive():
    global last_ping_time, next_ping_timestamp
    while True:
        driver = None
        try:
            print("🌐 Starting Headless Browser for Shahajjo Streamlit...")
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1280,800")
            chrome_options.binary_location = "/usr/bin/chromium"
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            
            print("🔗 Navigating to Shahajjo Streamlit App...")
            try:
                driver.get(STREAMLIT_URL)
            except Exception as load_err:
                print(f"⚠️ Page load timeout notice: {load_err}")

            print("⏳ Waiting 30 seconds for dynamic JS to render...")
            time.sleep(30)
            
            print("📜 Scroll Down (Human Behavior)...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            
            print("📜 Scroll Up (Human Behavior)...")
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)
            
            # Save screenshot and update timestamps
            driver.save_screenshot(SCREENSHOT_PATH)
            now_dt = datetime.now()
            last_ping_time = now_dt.strftime("%I:%M:%S %p (%d %b)")
            print(f"📸 Screenshot saved successfully at {last_ping_time}!")

        except Exception as e:
            print(f"⚠️ Automation Error: {e}")
        finally:
            if driver:
                driver.quit()
        
        # Set next execution time (5 minutes = 300 seconds)
        next_ping_timestamp = time.time() + 300
        print("💤 Waiting 5 minutes for next cycle...")
        time.sleep(300)

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
                margin-bottom: 20px;
                font-size: 15px;
                font-weight: bold;
                color: #744210;
                text-align: left;
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
            .refresh-btn {
                margin-top: 20px;
                background-color: #3182ce;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
            }
            .refresh-btn:hover {
                background-color: #2b6cb0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Shahajjo AI Keeper Dashboard</h1>
            <div class="subtitle">Automated Human-like Scroll & Sleep Prevention Bot</div>
            <div class="status-badge">🟢 Bot Active & Running 24/7</div>
            
            <div class="info-card">
                🕒 <strong>Last Successful Scroll:</strong> {{ last_time }}
            </div>

            <div class="timer-card">
                ⏳ <strong>Next Run In:</strong> <span id="countdown">Calculating...</span>
            </div>
            
            <div class="screenshot-box">
                <h3>📷 Live Streamlit App Window Preview:</h3>
                {% if has_image %}
                    <img src="/screenshot?t={{ timestamp }}" alt="Streamlit Live Screenshot">
                {% else %}
                    <p style="color: #e74c3c; font-weight: bold; font-size: 14px;">Prothom run cholche... 30-40 second pore page refresh korlei screenshot chole ashbe!</p>
                {% endif %}
            </div>
            
            <br>
            <a href="/" class="refresh-btn">🔄 Refresh Dashboard</a>
        </div>

        <script>
            var targetTime = {{ next_time }};
            
            function updateTimer() {
                if (targetTime === 0) {
                    document.getElementById("countdown").innerText = "Prothom run processing-e ache...";
                    return;
                }
                
                var now = Math.floor(Date.now() / 1000);
                var secondsLeft = targetTime - now;
                
                if (secondsLeft <= 0) {
                    document.getElementById("countdown").innerText = "Running now / Scroll cholche...";
                } else {
                    var mins = Math.floor(secondsLeft / 60);
                    var secs = secondsLeft % 60;
                    document.getElementById("countdown").innerText = mins + "m " + (secs < 10 ? "0" : "") + secs + "s";
                }
            }
            
            setInterval(updateTimer, 1000);
            updateTimer();
        </script>
    </body>
    </html>
    """
    has_image = os.path.exists(SCREENSHOT_PATH)
    timestamp = time.time()
    return render_template_string(
        html_template, 
        last_time=last_ping_time, 
        next_time=int(next_ping_timestamp), 
        has_image=has_image, 
        timestamp=timestamp
    )

@app.route("/screenshot")
def screenshot():
    if os.path.exists(SCREENSHOT_PATH):
        return send_file(SCREENSHOT_PATH, mimetype='image/png')
    return "Screenshot not ready yet.", 404

if __name__ == "__main__":
    # Initialize initial next run timestamp for countdown
    next_ping_timestamp = time.time() + 300
    
    t = threading.Thread(target=bot_scroll_and_keep_alive)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)