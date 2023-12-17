# chrome_factory.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ChromeFactory:
    @staticmethod
    def create_instance(use_profile=False):
        service_obj = Service(ChromeDriverManager().install())
        chrome_options = Options()

        if use_profile:
            profile_path = "/chrome-profile"
            chrome_options.add_argument(f'user-data-dir={profile_path}')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

        return webdriver.Chrome(service=service_obj, options=chrome_options)
