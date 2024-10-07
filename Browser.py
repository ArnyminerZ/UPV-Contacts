import logging

from selenium import webdriver

logger = logging.getLogger(__name__)

class Browser:
    def __init__(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        logger.debug("Initializing Firefox webdriver")
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        self.driver = webdriver.Firefox(options=options)

    def add_cookie(self, cookie_dict: dict):
        """
        This function adds a cookie to the browser.
        :param cookie_dict: The cookie to add.
        :return:
        """
        self.driver.add_cookie(cookie_dict)

    def create(self, url: str) -> webdriver.Firefox:
        """
        This function creates a new Firefox webdriver and opens the specified url
        :param url: The url to load.
        :return: The webdriver instance
        """
        self.driver.get(url)
        return self.driver

    def close(self):
        """
        This function closes the webdriver
        :return:
        """
        self.driver.close()
