# main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import base64
import io
from datetime import datetime, timedelta
import os

# For Speech-to-Text (install: pip install google-cloud-speech)
try:
    from google.cloud import speech_v1p1beta1 as speech
    SPEECH_ENABLED = True
except ImportError:
    SPEECH_ENABLED = False
    print("Install 'google-cloud-speech' for speech support.")

app = Flask(__name__)
CORS(app)

# === CONFIG ===
GOOGLE_API_KEY = "AIzaSyCxPh5Umy6Un20Gy3JtE5NoC7owNswRcJw"
GOOGLE_CX = "d2c3408b5c6d4402b"  # Replace with your CSE ID

# Google Cloud Speech (set env: export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json")
if SPEECH_ENABLED:
    speech_client = speech.SpeechClient()

# === Helper: Parse Discount from Text ===
def extract_discount(text):
    text = text.lower()
    patterns = [
        r'(\d+)%\s*off',
        r'save\s*(\d+)%',
        r'discount.*?(\d+)%',
        r'was\s*\$?([\d,]+\.?\d*)\s*now\s*\$?([\d,]+\.?\d*)',
        r'\$?([\d,]+\.?\d*)\s*[\–\-]\s*\$?([\d,]+\.?\d*)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            if '%' in match.group(0):
                percent = int(match.group(1))
                if percent >= 30:
                    return {"percent": percent, "type": "percent"}
            else:
                try:
                    original = float(match.group(1).replace(',', ''))
                    current = float(match.group(2).replace(',', ''))
                    if original > current:
                        percent = round(((original - current) / original) * 100)
                        if percent >= 30:
                            return {"percent": percent, "original": original, "current": current, "type": "price"}
                except:
                    pass
    return None

# === Unified Search Endpoint (Text or Processed Speech) ===
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        data = request.json
        query = data.get('query', '').strip()
    else:
        query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Enhance query for discounts
    enhanced_query = f"{query} discount pricing 30% off OR sale OR deal site:amazon.com OR site:bestbuy.com OR site:walmart.com"

    # Google Search
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": enhanced_query,
        "num": 10
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        items = data.get("items", [])
    except Exception as e:
        print("Google Search Error:", e)
        items = []

    # Parse for discounts and build response
    best_buys = []
    other_results = []
    for item in items:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        discount = extract_discount(snippet + " " + title)
        
        result = {
            "title": title[:100] + "..." if len(title) > 100 else title,
            "snippet": snippet[:150] + "..." if len(snippet) > 150 else snippet,
            "url": link,
            "discount": discount
        }
        
        if discount and discount.get("percent", 0) >= 30:
            best_buys.append(result)
        else:
            other_results.append(result)

    response = {
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "best_buys": best_buys[:5],  # Top 5 deals ≥30% off
        "other_results": other_results[:5],  # Other relevant
        "total_results": len(items)
    }

    return jsonify(response)

# === Speech-to-Text Endpoint ===
@app.route('/speech', methods=['POST'])
def speech_to_text():
    if not SPEECH_ENABLED:
        return jsonify({"error": "Speech support not installed. Install google-cloud-speech."}), 500

    try:
        data = request.json
        audio_base64 = data.get('audio', '')  # Base64-encoded audio (WAV/MP3)
        if not audio_base64:
            return jsonify({"error": "No audio provided"}), 400

        # Decode base64 to bytes
        audio_bytes = base64.b64decode(audio_base64)

        # Configure audio
        audio = speech.RecognitionAudio(content=audio_bytes)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Adjust for your format
            sample_rate_hertz=16000,
            language_code="en-US",
        )

        # Transcribe
        response = speech_client.recognize(config=config, audio=audio)
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "

        transcript = transcript.strip()
        if not transcript:
            return jsonify({"error": "No speech detected"}), 400

        # Forward to search
        search_response = search()  # Reuse search logic (returns jsonify)
        search_data = search_response.get_json()

        return jsonify({
            "transcript": transcript,
            "search_results": search_data
        })

    except Exception as e:
        print("Speech Error:", e)
        return jsonify({"error": str(e)}), 500

# === Health Check ===
@app.route('/')
def home():
    return jsonify({
        "message": "AI Discount Search Backend Running!",
        "endpoints": {
            "text_search": "GET/POST /search?q=product_name or {'query': 'product_name'}",
            "speech_search": "POST /speech {'audio': 'base64_audio'}"
        },
        "speech_note": "Set GOOGLE_APPLICATION_CREDENTIALS for speech."
    })

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
