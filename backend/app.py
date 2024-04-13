from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from flask_cors import CORS
from urllib.parse import urlparse
from collections import Counter
import requests
import re
import stopwordsiso as stopwords
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)
# CORS setup...
CORS(app)

def extract_canonical_tag(soup):
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    canonical_url = canonical_tag['href'] if canonical_tag else None
    return canonical_url

def measure_response_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    response_time = end_time - start_time
    return response_time

def measure_page_size(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text content from <html> and <body> tags
    html_body_text = ' '.join(tag.get_text() for tag in soup.find_all(['html', 'body']))
    
    # Calculate size of text content in kilobytes
    size_in_bytes = len(html_body_text.encode('utf-8'))
    size_in_kb = size_in_bytes / 1024  # Convert bytes to kilobytes
    
    return size_in_kb

def take_mobile_snapshot(url):
    save_fn = "mobile-snapshot.png"

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--auto-open-devtools-for-tabs")

    # Set up mobile emulation
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 XL Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36")

    driver = webdriver.Firefox(options=options)

    # Set window size to match mobile device (Samsung Galaxy S9)
    driver.set_window_size(360, 740)

    driver.get(url)
    
    # Wait for the page to fully load (adjust the delay as needed)
    time.sleep(1)

    print(driver.title)

    # Take screenshot
    driver.save_screenshot(save_fn)

    driver.quit()

    return save_fn

def take_search_result_snapshot(url):
    search_query = url

    save_fn = "search-results.png"

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Firefox(options=options)

    # Perform a search query using Firefox address bar
    search_url = f"https://www.google.com/search?q={search_query}"
    driver.get(search_url)

    # Wait for search results to load
    time.sleep(1)

    # Click on the "Přijmout vše" button
    accept_button = driver.find_element(By.ID, "L2AGLb")
    accept_button.click()

    driver.save_screenshot(save_fn)

    driver.quit()

    return save_fn

def is_directory_listing_disabled(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Check if the response contains directory listing
            if "Index of" in response.text:
                return False
            else:
                return True
        else:
            return False
    except Exception as e:
        print(f"Error checking directory listing: {e}")
        return False
    
def is_https_enabled(url):
    try:
        response = requests.get(url)
        return response.url.startswith("https")
    except Exception as e:
        print(f"Error checking HTTPS: {e}")
        return False

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

        # Extract canonical tag
        canonical_url = extract_canonical_tag(soup)

        # Measure response time
        # The response time of your homepage is 0.xx seconds. It is recommended to keep it equal to or below 0.2 seconds.
        response_time = measure_response_time(url)

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

        ### EXTRACT PAGE SIZE ###
        # Ideally, keep the HTML page size around 100 kB or less.
        # In some cases (like ecommerce) it's ok to have pages around 150kB-200kB
        page_size = measure_page_size(response.text)

        ### TAKE MOBILE SNAPSHOT ###
        mobile_snapshot_path = take_mobile_snapshot(url)

        ### WEB BROWSER PREVIEW ###
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
