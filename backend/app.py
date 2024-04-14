from flask import Flask, jsonify, request
from flask_cors import CORS
from web_analysis import *
from screenshot import *
import requests

app = Flask(__name__)
# CORS setup...
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_url():
    data = request.json
    url = data.get('url')

    try:
        # Send HTTP GET request to fetch webpage content
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch webpage content'}), 400

        soup = BeautifulSoup(response.text, 'html.parser')

        canonical_url = extract_canonical_tag(soup)
        response_time = measure_response_time(url)

        title_tag = extract_title_tag(soup)
        title_length = len(title_tag)

        meta_description_content = extract_meta_description_content(soup)
        meta_description_length = len(meta_description_content)

        headings = extract_heading_tags(soup)
        h1_number = len(headings.get('H1'))
        h2_number = len(headings.get('H2'))

        images_without_alt = extract_images_without_alt(soup)
        images_without_alt_number = len(images_without_alt)

        internal_links, external_links = extract_links(url, soup)
        internal_links_number = len(internal_links)
        external_links_number = len(external_links)

        most_common_keywords = extract_most_common_keywords(soup)

        page_size = measure_page_size(response.text)

        mobile_snapshot_path = take_mobile_snapshot(url)
        search_result_snapshot = take_search_result_snapshot(url)

        directory_listing_disabled = is_directory_listing_disabled(url)
        https_enabled = is_https_enabled(url)

        # Prepare analysis report
        report = {
            'canonical_url': canonical_url,
            'response_time': response_time,
            'title': title_tag,
            'title_length': title_length,
            'meta_description': meta_description_content,
            'meta_description_length': meta_description_length,
            'headings': headings,
            'h1_number': h1_number,
            'h2_number': h2_number,
            'images_without_alt': images_without_alt,
            'images_without_alt_number': images_without_alt_number,
            'internal_links': internal_links,
            'external_links': external_links,
            'internal_links_number': internal_links_number,
            'external_links_number': external_links_number,
            'keyword_frequency': most_common_keywords,
            'page_size': page_size,
            'mobile_snapshot_path': mobile_snapshot_path,
            'search_result_snapshot': search_result_snapshot,
            'directory_listing_disabled': directory_listing_disabled,
            'https_enabled': https_enabled
        }

        # Save report to file
        with open('report.txt', 'w') as f:
            for key, value in report.items():
                f.write(f'{key}: {value}\n')
        
        return jsonify(report), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
