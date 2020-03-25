from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
import json


class Browser:
    CONFIG_FILE = '..\\config.json'

    def __init__(self):
        self._driver = None
        self._json_data = None

    def start(self):
        with open(self.CONFIG_FILE) as file:
            self._json_data = json.loads(file.read())
        if self._json_data["browser"] == "Chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--no-proxy-server')
            chrome_options.add_argument("--disable-extensions")
            self._driver = webdriver.Chrome(chrome_options=chrome_options)
        elif self._json_data["browser"] == "FF":
            self._driver = webdriver.Firefox()

    def stop(self):
        self._driver.quit()

    @property
    def driver(self):
        return self._driver

    @property
    def json_data(self):
        return self._json_data

    def get(self, url):
        self._driver.get(url)

    def get_element(self, element_def, timeout=5):
        try:
            el = WebDriverWait(self._driver, timeout).until(lambda d: d.find_element_by_xpath(element_def['xpath']))
        except TimeoutException or NoSuchElementException:
            raise AssertionError('Element not found')

        return el

    def maximize_window(self):
        self._driver.maximize_window()

    def hover(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()




