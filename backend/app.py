from flask import Flask, jsonify, request
from flask_cors import CORS
from web_analysis import WebAnalyzer

app = Flask(__name__)
# CORS setup...
CORS(app)

web_analyzer = WebAnalyzer(app)

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
