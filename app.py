# -*- coding: utf-8 -*-
import os
import time
import threading
from datetime import datetime
from flask import Flask, send_file, render_template_string, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageDraw

app = Flask(__name__)

STREAMLIT_URL = "https://shahajjo.streamlit.app/"
SCREENSHOT_PATH = "latest_status.png"

last_ping_time = "Ekhono kono session complete hoyni"
next_ping_timestamp = 0
last_error_message = "Kono error nei (Bot start hocche...)"

def create_initial_placeholder():
    if not os.path.exists(SCREENSHOT_PATH):
        try:
            img = Image.new('RGB', (1280, 800), color='#0f172a')
            d = ImageDraw.Draw(img)
            d.text((380, 380), "Shahajjo Bot Starting... Firefox SS Loading...", fill=(255, 255, 255))
            img.save(SCREENSHOT_PATH)
        except Exception as e:
            print(f"Placeholder error: {e}")

create_initial_placeholder()

def bot_scroll_and_keep_alive():
    global last_ping_time, next_ping_timestamp, last_error_message
    while True:
        driver = None
        try:
            print("🚀 Selenium Firefox start hocche...")
            firefox_options = Options()
            firefox_options.add_argument("--headless")
            firefox_options.binary_location = "/usr/bin/firefox-esr"
            
            driver = webdriver.Firefox(options=firefox_options)
            driver.set_window_size(1280, 800)
            driver.set_page_load_timeout(90)
            
            print(f"🌐 Navigating to {STREAMLIT_URL}...")
            driver.get(STREAMLIT_URL)
            
            print("⏳ Waiting 45 seconds for Streamlit dynamic JS to load...")
            time.sleep(45)
            
            print("📜 Scrolling down (Human behavior simulation)...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            
            print("📜 Scrolling up...")
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)
            
            print("📸 Capturing screenshot...")
            driver.save_screenshot(SCREENSHOT_PATH)
            
            last_ping_time = datetime.now().strftime("%I:%M:%S %p (%d %b)")
            last_error_message = "Kono error nei (Successfully captured with Firefox)"
            print(f"✅ Success! Screenshot saved at {last_ping_time}")

        except Exception as e:
            last_error_message = str(e)
            print(f"⚠️ Firefox Automation Error: {e}")
        finally:
            if driver:
                driver.quit()
        
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
            .error-card {
                background: #fff5f5;
                border-left: 4px solid #e53e3e;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 15px;
                font-size: 13px;
                text-align: left;
                color: #c53030;
                word-break: break-all;
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Shahajjo AI Keeper Dashboard</h1>
            <div class="subtitle">Firefox Automated Scroll & Live Preview Bot</div>
            <div class="status-badge">🟢 Bot Active & Running 24/7</div>
            
            <div class="info-card">
                🕒 <strong>Last Successful Scroll:</strong> <span id="last-time">{{ last_time }}</span>
            </div>

            <div class="timer-card">
                ⏳ <strong>Next Run In:</strong> <span id="countdown">Calculating...</span>
            </div>

            <div class="error-card">
                ⚠️ <strong>Last Status / Error Log:</strong> <span id="error-log">{{ error_msg }}</span>
            </div>
            
            <div class="screenshot-box">
                <h3>📷 Live Streamlit App Window Preview:</h3>
                <div id="image-container">
                    <img id="live-ss" src="/screenshot?t={{ timestamp }}" alt="Streamlit Live Screenshot">
                </div>
            </div>
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

            function autoRefreshData() {
                fetch('/status-json')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("last-time").innerText = data.last_time;
                        document.getElementById("error-log").innerText = data.error_msg;
                        
                        var imgElem = document.getElementById("live-ss");
                        if (imgElem) {
                            imgElem.src = "/screenshot?t=" + Date.now();
                        }
                    })
                    .catch(err => console.log('Fetch error:', err));
            }

            setInterval(autoRefreshData, 10000);
        </script>
    </body>
    </html>
    """
    timestamp = time.time()
    return render_template_string(
        html_template, 
        last_time=last_ping_time, 
        next_time=int(next_ping_timestamp), 
        error_msg=last_error_message,
        timestamp=timestamp
    )

@app.route("/status-json")
def status_json():
    return jsonify({
        "last_time": last_ping_time,
        "error_msg": last_error_message
    })

@app.route("/screenshot")
def screenshot():
    if os.path.exists(SCREENSHOT_PATH):
        return send_file(SCREENSHOT_PATH, mimetype='image/png')
    return "Screenshot not ready yet.", 404

if __name__ == "__main__":
    next_ping_timestamp = time.time() + 300
    
    t = threading.Thread(target=bot_scroll_and_keep_alive)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
