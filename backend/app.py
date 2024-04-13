from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from flask_cors import CORS
from urllib.parse import urlparse
from collections import Counter
import requests
import re
import stopwordsiso as stopwords


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

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        ### EXTRACT TITLE TAG
        # title tag should be between 30 to 60 characters long
        title_tag = soup.title.string.strip() if soup.title else None
        title_length = len(title_tag)

        ### EXTRACT META DESCRIPTION
        # between 50 and 160 characters long
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'].strip() if meta_description else None
        meta_description_length = len(meta_description_content)

        ### EXTRACT HEADING TAGS (H1, H2, etc.)
        # H1 should be only one, H2 does not matter (use them to better structure your page so it flows better)
        headings = {}
        for heading_level in range(1, 3):
            headings[f'H{heading_level}'] = [heading.text.strip() for heading in soup.find_all(f'h{heading_level}')]
        
        h1_number = len(headings.get('H1'))
        h2_number = len(headings.get('H2'))

        ### EXTRACT IMAGE TAGS without alt attribute
        # add useful descriptions to each image
        # Some images on your homepage have no alt attribute. (112)
        images_without_alt = [img['src'] for img in soup.find_all('img') if not img.get('alt')]
        images_without_alt_number = len(images_without_alt)

        ### EXTRACT internal and external links
        # As for the ratio, there isn't a strict rule, but a common recommendation is to have more internal links than external links. A rough guideline could be to aim for a ratio of around 2:1 or 3:1 of internal links to external links. However, the most important factor is the relevance and context of the links rather than the specific ratio. Focus on providing value to your users and ensuring that your linking strategy enhances their experience and supports your SEO objectives.
        # -> more internal than external will be ok
        internal_links = []
        external_links = []
        parsed_url = urlparse(url)

        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('#'):
                continue  # Skip internal anchor links

            parsed_href = urlparse(href)

            # Check if the link has a netloc (domain)
            if parsed_href.netloc:
                # Check if the netloc matches the base URL's netloc
                if parsed_href.netloc == parsed_url.netloc:
                    internal_links.append(href)
                else:
                    external_links.append(href)
            else:
                # If the link doesn't have a netloc, it's a relative link
                internal_links.append(href)

        internal_links_number = len(internal_links)
        external_links_number = len(external_links)

        # EXTRACT TEXT content and calculate keyword frequency
        # Just informative
        # Here are the most common keywords we found on your homepage (10 keywords)
        # Extract text content
        text_content = soup.get_text()

        # Tokenize the text by splitting it into words (assuming words are separated by whitespace)
        words = re.findall(r'\b\w+\b', text_content.lower())  # Extract words and convert to lowercase

        additional_stopwords = set([
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "00", "01"
        ])

        # Filter out stopwords
        filtered_words_cs = [word for word in words if word not in (stopwords.stopwords("cs"))]
        filtered_words_cs_en = [word for word in filtered_words_cs if word not in (stopwords.stopwords("en"))]
        filtered_words = [word for word in filtered_words_cs_en if word not in additional_stopwords]

        # Calculate word frequency
        word_freq = Counter(filtered_words)

        most_common_keywords = word_freq.most_common(10)

        for keyword, frequency in most_common_keywords:
            print(keyword, ":", frequency)

        # Prepare analysis report
        report = {
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
            'keyword_frequency': most_common_keywords
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
