from flask import Flask, render_template, request, jsonify
import os
import base64
from datetime import datetime

app = Flask(__name__)

SAVE_DIR = os.path.join(os.path.dirname(__file__), 'media')
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data_url = request.json.get('video') or request.json.get('image')
    if not data_url:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    header, encoded = data_url.split(',', 1)
    if 'mp4' in header:
        file_ext = 'mp4'
    elif 'webm' in header:
        file_ext = 'webm'
    else:
        file_ext = 'png'

    try:
        file_data = base64.b64decode(encoded)
    except Exception:
        return jsonify({'success': False, 'error': 'Decoding failed'}), 400

    filename = datetime.utcnow().strftime('%Y%m%d_%H%M%S') + f'.{file_ext}'
    path = os.path.join(SAVE_DIR, filename)
    with open(path, 'wb') as f:
        f.write(file_data)

    return jsonify({'success': True, 'filename': filename})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 locally if PORT not set
    app.run(host="0.0.0.0", port=port)
