import time
import re
import requests
import stopwordsiso as stopwords
from bs4 import BeautifulSoup
from collections import Counter
from flask import jsonify
from urllib.parse import urlparse
from screenshot import *

from flask_cors import CORS


class WebAnalyzer:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        CORS(app)

    def my_len(self, text):
        if text is None:
            return 0
        
        return len(text)

    def extract_canonical_tag(self, soup):
        """
        Extracts the canonical URL from the given BeautifulSoup object representing a webpage. Passed - if the webpage is using canonical tag, Failed - not using.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the webpage.

        Returns:
            str: The canonical URL, or None if not found.
        """
        canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
        canonical_url = canonical_tag['href'] if canonical_tag else None
        return canonical_url
    
    def test_canonical_url(self, canonical_url, results):
        if canonical_url is None:
            results['failed'] += 1
            return "failed"
        else:
            results['passed'] += 1
            return "passed"

    def measure_response_time(self, url):
        """
        Measures the response time of a given URL. Passed - below 0.2 seconds, Warning - from 0.2 to 1s, Failed - more than 1s.

        Parameters:
            url (str): The URL to measure the response time for.

        Returns:
            float: The response time in seconds.
        """
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        response_time = end_time - start_time
        return response_time
    
    def test_response_time(self, response_time, results):
        if response_time <= 0.2:
            results['passed'] += 1
            return "passed"
        elif response_time <= 1:
            results['warning'] += 1
            return "warning"
        else:
            results['failed'] += 1
            return "failed"

    def extract_title_tag(self, soup):
        """
        Extracts the title tag from the given BeautifulSoup object representing a webpage. Passed - 30 to 60 characters long, Failed - else.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the webpage.

        Returns:
            str: The content of the title tag, or None if not found.
        """
        return soup.title.string.strip() if soup.title else None
    
    def test_title_length(self, title_length, results):
        if title_length >= 30 and title_length <= 60:
            results['passed'] += 1
            return "passed"
        if title_length >= 25 and title_length <= 65:
            results['warning'] += 1
            return "warning"
        else:
            results['failed'] += 1
            return "failed"

    def extract_meta_description_content(self, soup):
        """
        Extracts the content of the meta description tag from the given BeautifulSoup object representing a webpage. Passed - between 50 and 160 characters long, Failed - else.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the webpage.

        Returns:
            str: The content of the meta description tag, or None if not found.
        """
        meta_description = soup.find('meta', attrs={'name': 'description'})
        return meta_description['content'].strip() if meta_description else None
    
    def test_meta_description_length(self, meta_description_length, results):
        if meta_description_length >= 50 and meta_description_length <= 160:
            results['passed'] += 1
            return "passed"
        if meta_description_length >= 45 and meta_description_length <= 165:
            results['warning'] += 1
            return "warning"
        else:
            results['failed'] += 1
            return "failed"

    # H1 should be only one, H2 does not matter (use them to better structure your page so it flows better)
    def extract_heading_tags(self, soup):
        """
        Extracts the content of heading tags (H1, H2, etc.) from the given BeautifulSoup object representing a webpage. Amount of H1 Passed - 1, Failed - else. Amount of H2 Informative

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the webpage.

        Returns:
            dict: A dictionary containing the content of heading tags as values and their corresponding tag names (H1, H2, etc.) as keys.
        """
        headings = {}
        for heading_level in range(1, 3):
            headings[f'H{heading_level}'] = [heading.text.strip() for heading in soup.find_all(f'h{heading_level}')]

        return headings
    
    def test_h1_number(self, h1_number, results):
        if h1_number == 1:
            results['passed'] += 1
            return "passed"
        else:
            results['failed'] += 1
            return "failed"

    ### EXTRACT IMAGE TAGS without alt attribute
    # add useful descriptions to each image
    # Some images on your homepage have no alt attribute. (112)
    def extract_images_without_alt(self, soup):
        return [img['src'] for img in soup.find_all('img') if not img.get('alt')]
    
    def test_images_without_alt_number(self, images_without_alt_number, results):
        if images_without_alt_number == 0:
            results['passed'] += 1
            return "passed"
        else:
            results['failed'] += 1
            return "failed"

    ### EXTRACT internal and external links
    # As for the ratio, there isn't a strict rule, but a common recommendation is to have more internal links than external links. A rough guideline could be to aim for a ratio of around 2:1 or 3:1 of internal links to external links. However, the most important factor is the relevance and context of the links rather than the specific ratio. Focus on providing value to your users and ensuring that your linking strategy enhances their experience and supports your SEO objectives.
    # -> more internal than external will be ok
    def extract_links(self, url, soup):
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

        return internal_links, external_links
    
    def test_links_number_ratio(self, internal_links_number, external_links_number, results):
        if internal_links_number > external_links_number:
            results['passed'] += 1
            return "passed"
        else:
            results['warning'] += 1
            return "warning"

    # EXTRACT TEXT content and calculate keyword frequency
    # Just informative
    # Here are the most common keywords we found on your homepage (10 keywords)
    # Extract text content
    def extract_most_common_keywords(self, soup):
        text_content = soup.get_text()

        # Tokenize the text by splitting it into words (assuming words are separated by whitespace)
        words = re.findall(r'\b\w+\b', text_content.lower())  # Extract words and convert to lowercase

        additional_stopwords = set([
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "00", "01", '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'
        ])

        # Filter out stopwords
        filtered_words_cs = [word for word in words if word not in (stopwords.stopwords("cs"))]
        filtered_words_cs_en = [word for word in filtered_words_cs if word not in (stopwords.stopwords("en"))]
        filtered_words = [word for word in filtered_words_cs_en if word not in additional_stopwords]

        # Calculate word frequency
        word_freq = Counter(filtered_words)

        return word_freq.most_common(10)

    ### EXTRACT PAGE SIZE ###
    # Ideally, keep the HTML page size around 100 kB or less.
    # In some cases (like ecommerce) it's ok to have pages around 150kB-200kB
    def measure_page_size(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text content from <html> and <body> tags
        html_body_text = ' '.join(tag.get_text() for tag in soup.find_all(['html', 'body']))
        
        # Calculate size of text content in kilobytes
        size_in_bytes = len(html_body_text.encode('utf-8'))
        size_in_kb = size_in_bytes / 1024  # Convert bytes to kilobytes
        
        return size_in_kb
    
    def test_page_size(self, page_size, results):
        if page_size <= 100:
            results['passed'] += 1
            return "passed"
        if page_size <= 200:
            results['warning'] += 1
            return "warning"
        else:
            results['failed'] += 1
            return "failed"

    def is_directory_listing_disabled(self, url):
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
        
    def test_directory_listing_disabled(self, directory_listing_disabled, results):
        if directory_listing_disabled is True:
            results['passed'] += 1
            return "passed"
        else:
            results['failed'] += 1
            return "failed"
        
    def is_https_enabled(self, url):
        try:
            response = requests.get(url)
            return response.url.startswith("https")
        except Exception as e:
            print(f"Error checking HTTPS: {e}")
            return False
        
    def test_https_enabled(self, https_enabled, results):
        if https_enabled is True:
            results['passed'] += 1
            return "passed"
        else:
            results['failed'] += 1
            return "failed"
        
    def analyze(self, url):
        # Send HTTP GET request to fetch webpage content
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch webpage content'}), 400

        screenshot_taker = ScreenshotTaker()
        results = {'passed': 0, 'warning': 0, 'failed': 0}
        soup = BeautifulSoup(response.text, 'html.parser')

        canonical_url = self.extract_canonical_tag(soup)
        canonical_url_test = self.test_canonical_url(canonical_url, results)
        response_time = self.measure_response_time(url)
        response_time_test = self.test_response_time(response_time, results)

        title_tag = self.extract_title_tag(soup)
        title_length = self.my_len(title_tag)
        title_length_test = self.test_title_length(title_length, results)

        meta_description_content = self.extract_meta_description_content(soup)
        meta_description_length = self.my_len(meta_description_content)
        meta_description_length_test = self.test_meta_description_length(meta_description_length, results)

        headings = self.extract_heading_tags(soup)
        h1_number = len(headings.get('H1'))
        h2_number = len(headings.get('H2'))
        h1_number_test = self.test_h1_number(h1_number, results)
        h2_number_test = "informative"

        images_without_alt = self.extract_images_without_alt(soup)
        images_without_alt_number = len(images_without_alt)
        images_without_alt_number_test = self.test_images_without_alt_number(images_without_alt_number, results)

        internal_links, external_links = self.extract_links(url, soup)
        internal_links_number = len(internal_links)
        external_links_number = len(external_links)
        links_number_ratio_test = self.test_links_number_ratio(internal_links_number, external_links_number, results)

        most_common_keywords = self.extract_most_common_keywords(soup)
        most_common_keywords_test = "informative"

        page_size = self.measure_page_size(response.text)
        page_size_test = self.test_page_size(page_size, results)

        mobile_snapshot_path = screenshot_taker.take_mobile_snapshot(url)

        # this result not needed in frontend for now and because it takes a lot of time -> commented
        # search_result_snapshot = screenshot_taker.take_search_result_snapshot(url)
        search_result_snapshot = None

        mobile_snapshot_path_test = "informative"
        search_result_snapshot_test = "informative"

        directory_listing_disabled = self.is_directory_listing_disabled(url)
        directory_listing_disabled_test = self.test_directory_listing_disabled(directory_listing_disabled, results)
        https_enabled = self.is_https_enabled(url)
        https_enabled_test = self.test_https_enabled(https_enabled, results)

        # Prepare analysis report
        report = {
            'canonical_url': canonical_url,
            'canonical_url_test': canonical_url_test,
            'response_time': response_time,
            'response_time_test': response_time_test,
            'title': title_tag,
            'title_length': title_length,
            'title_length_test': title_length_test,
            'meta_description': meta_description_content,
            'meta_description_length': meta_description_length,
            'meta_description_length_test': meta_description_length_test,
            'headings': headings,
            'h1_number': h1_number,
            'h2_number': h2_number,
            'h1_number_test': h1_number_test,
            'h2_number_test': h2_number_test,
            'images_without_alt': images_without_alt,
            'images_without_alt_number': images_without_alt_number,
            'images_without_alt_number_test': images_without_alt_number_test,
            'internal_links': internal_links,
            'external_links': external_links,
            'internal_links_number': internal_links_number,
            'external_links_number': external_links_number,
            'links_number_ratio_test': links_number_ratio_test,
            'keyword_frequency': most_common_keywords,
            'most_common_keywords_test': most_common_keywords_test,
            'page_size': page_size,
            'page_size_test': page_size_test,
            'mobile_snapshot_path': mobile_snapshot_path,
            'mobile_snapshot_path_test': mobile_snapshot_path_test,
            'search_result_snapshot': search_result_snapshot,
            'search_result_snapshot_test': search_result_snapshot_test,
            'directory_listing_disabled': directory_listing_disabled,
            'directory_listing_disabled_test': directory_listing_disabled_test,
            'https_enabled': https_enabled,
            'https_enabled_test': https_enabled_test,
            'results': results
        }

        # Save report to file
        with open('report.txt', 'w') as f:
            for key, value in report.items():
                f.write(f'{key}: {value}\n')
        
        return report
