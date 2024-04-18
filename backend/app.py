import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from web_analysis import WebAnalyzer

app = Flask(__name__)
# CORS setup...
CORS(app)

web_analyzer = WebAnalyzer(app)

# Serve images from the 'backend' folder
@app.route('/images/mobile-snapshot.png')
def serve_mobile_snapshot():
    return send_from_directory('.', 'mobile-snapshot.png')

@app.route('/analyze', methods=['POST'])
def analyze_url():
    data = request.json
    url = data.get('url')

    try:
        report = web_analyzer.analyze(url)
        return jsonify(report), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
