import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class ScreenshotTaker:
    ### TAKE MOBILE SNAPSHOT ###
    def take_mobile_snapshot(self, url):
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
        
        # Wait for the page to fully load
        time.sleep(1)

        # Take screenshot
        driver.save_screenshot(save_fn)
        driver.quit()

        return save_fn

    ### WEB BROWSER PREVIEW ###
    def take_search_result_snapshot(self, url):
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

        # Click on the "Accept everything" button
        accept_button = driver.find_element(By.ID, "L2AGLb")
        accept_button.click()

        driver.save_screenshot(save_fn)
        driver.quit()

        return save_fn
