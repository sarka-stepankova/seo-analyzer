import time
import re
import requests
import stopwordsiso as stopwords
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urlparse

def extract_canonical_tag(soup):
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    canonical_url = canonical_tag['href'] if canonical_tag else None
    return canonical_url

# Measure response time
# The response time of your homepage is 0.xx seconds. It is recommended to keep it equal to or below 0.2 seconds.
def measure_response_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    response_time = end_time - start_time
    return response_time

### EXTRACT TITLE TAG
# title tag should be between 30 to 60 characters long
def extract_title_tag(soup):
    return soup.title.string.strip() if soup.title else None

### EXTRACT META DESCRIPTION
# between 50 and 160 characters long
def extract_meta_description_content(soup):
    meta_description = soup.find('meta', attrs={'name': 'description'})
    return meta_description['content'].strip() if meta_description else None

### EXTRACT HEADING TAGS (H1, H2, etc.)
# H1 should be only one, H2 does not matter (use them to better structure your page so it flows better)
def extract_heading_tags(soup):
    headings = {}
    for heading_level in range(1, 3):
        headings[f'H{heading_level}'] = [heading.text.strip() for heading in soup.find_all(f'h{heading_level}')]

    return headings

### EXTRACT IMAGE TAGS without alt attribute
# add useful descriptions to each image
# Some images on your homepage have no alt attribute. (112)
def extract_images_without_alt(soup):
    return [img['src'] for img in soup.find_all('img') if not img.get('alt')]

### EXTRACT internal and external links
# As for the ratio, there isn't a strict rule, but a common recommendation is to have more internal links than external links. A rough guideline could be to aim for a ratio of around 2:1 or 3:1 of internal links to external links. However, the most important factor is the relevance and context of the links rather than the specific ratio. Focus on providing value to your users and ensuring that your linking strategy enhances their experience and supports your SEO objectives.
# -> more internal than external will be ok
def extract_links(url, soup):
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

# EXTRACT TEXT content and calculate keyword frequency
# Just informative
# Here are the most common keywords we found on your homepage (10 keywords)
# Extract text content
def extract_most_common_keywords(soup):
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

    return word_freq.most_common(10)

### EXTRACT PAGE SIZE ###
# Ideally, keep the HTML page size around 100 kB or less.
# In some cases (like ecommerce) it's ok to have pages around 150kB-200kB
def measure_page_size(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text content from <html> and <body> tags
    html_body_text = ' '.join(tag.get_text() for tag in soup.find_all(['html', 'body']))
    
    # Calculate size of text content in kilobytes
    size_in_bytes = len(html_body_text.encode('utf-8'))
    size_in_kb = size_in_bytes / 1024  # Convert bytes to kilobytes
    
    return size_in_kb

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
