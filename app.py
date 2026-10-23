# -*- coding: utf-8 -*-
import os
import time
import threading
from flask import Flask, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Apnar main Streamlit App-er sothik URL
STREAMLIT_URL = "https://shahajjo.streamlit.app/"
SCREENSHOT_PATH = "latest_status.png"

def bot_scroll_and_keep_alive():
    """Prottee 5 minute por por headless browser chalye Streamlit awake rakhbe"""
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
            driver.get(STREAMLIT_URL)
            
            print("⏳ Waiting 30 seconds for Streamlit to fully load...")
            time.sleep(30)
            
            print("📜 Scrolling Down...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            print("📜 Scrolling Up...")
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)
            
            # Status check er jonno screenshot save hobe
            driver.save_screenshot(SCREENSHOT_PATH)
            print("📸 Screenshot captured successfully!")

        except Exception as e:
            print(f"⚠️ Browser automation error: {e}")
        finally:
            if driver:
                driver.quit()
        
        # Exact 5 minutes (300 seconds) por por abar run hobe
        print("💤 Waiting 5 minutes before next session...")
        time.sleep(300)

@app.route("/")
def home():
    return """
    <h1>🚀 Shahajjo Streamlit Keeper Running 24/7!</h1>
    <p>View live screenshot of Streamlit: <a href="/screenshot">/screenshot</a></p>
    """

@app.route("/screenshot")
def screenshot():
    if os.path.exists(SCREENSHOT_PATH):
        return send_file(SCREENSHOT_PATH, mimetype='image/png')
    return "Screenshot not ready yet. Please wait a moment."

if __name__ == "__main__":
    # Background-e automation thread start kora hocche
    t = threading.Thread(target=bot_scroll_and_keep_alive)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
