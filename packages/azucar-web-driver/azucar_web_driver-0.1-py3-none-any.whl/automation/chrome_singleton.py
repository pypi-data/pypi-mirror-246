# chrome_singleton.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ChromeSingleton:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            chrome_path = "/chrome-profile"
            service_obj = Service(ChromeDriverManager().install())
            chrome_options = Options()
            chrome_options.add_argument(f'user-data-dir={chrome_path}')
            cls.instance = webdriver.Chrome(service=service_obj, options=chrome_options)
        return cls.instance
