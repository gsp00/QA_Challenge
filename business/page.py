import json
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from business.table import Table


class Page(object):
    def __init__(self, browser, page_name='Home'):
        self._browser = browser
        self.page_name = page_name
        self._elements_definitions = None
        self._load_elements_def()

    @property
    def browser(self):
        return self._browser

    def _get_element(self, element_name, timeout=5):
        element_def = self._get_element_def(element_name)
        return self._browser.get_element(element_def, timeout)

    def _load_elements_def(self):
        elements_json_folder = self._browser.json_data["defs_folder"]
        path = os.path.join(elements_json_folder, self.page_name + '.json')
        if os.path.exists(path):
            with open(path) as file:
                self._elements_definitions = json.loads(file.read())
        else:
            raise AssertionError('Elements definition file for page {} not found'.format(self.page_name))

    def _get_element_def(self, element_name):
        return self._elements_definitions.get(element_name, None)

    def write(self, element_name, text):
        el = self._get_element(element_name)
        el.clear()
        el.send_keys(text)

    def wait(self, seconds):
        time.sleep(seconds)

    def click(self, element_name):
        el = self._get_element(element_name)
        try:
            el.click()
        except ElementNotInteractableException:
            self._browser.driver.execute_script('arguments[0].click()', el)

    def _wait_for_element(self, element_name, timeout=5):
        el = self._get_element(element_name, timeout)
        if not el:
            raise AssertionError("Element not found: {element}".format(element=element_name))
        return el

    def wait_title_is(self, page_title, timeout=5):
        wait = WebDriverWait(self._browser.driver, timeout)
        wait.until(EC.title_is(page_title))

    def wait_element_is_visible(self, element_name, xpath=None, timeout=5):
        if element_name:
            self._wait_for_element(element_name, timeout)
        elif xpath:
            wait = WebDriverWait(self._browser.driver, timeout)
            wait.until(EC.visibility_of_element_located(By.XPATH(xpath)))

    def wait_element_is_clickable(self, element_name, xpath=None, timeout=5):
        def get_el(self, el_name, seconds):
            elm = self._wait_for_element(el_name, seconds)
            return elm.is_enabled()

        is_clickable = False
        if element_name:
            for _ in range(timeout):
                is_clickable = get_el(self, element_name, timeout)
                if is_clickable:
                    break
                time.sleep(1)
            if not is_clickable:
                raise AssertionError('Element not clickable')
        elif xpath:
            wait = WebDriverWait(self._browser.driver, timeout)
            wait.until(EC.element_to_be_clickable(By.XPATH(xpath)))

    def press_key(self, element_name, key):
        el = self._get_element(element_name)
        special_key = getattr(Keys, key.upper(), None)
        el.send_keys(special_key)

    def hover(self, element_name=None, xpath=None):
        if element_name:
            el = self._get_element(element_name)
        elif xpath:
            try:
                el = self._browser.driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                raise AssertionError('Element not found')

        if el:
            self._browser.hover(el)

    def get_table(self, table_name):
        table_def = self._get_element_def(table_name)
        if table_def:
            table = Table(self._browser, table_name, table_def)
        else:
            raise AssertionError('Definition for {table} not found'.format(table=table_name))

        return table












