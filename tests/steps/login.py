from base.browser import Browser
from business.page import Page
import json


def open_site_and_login():
    file_path = '..\\test_data\\environment.json'
    with open(file_path) as file:
        data = json.loads(file.read())
        if data:
            browser = Browser()
            browser.start()
            browser.get(data['url'])
            browser.maximize_window()
            top_menu = Page(browser, 'Top Menu')
            top_menu.click('Sign in')
            top_menu.wait_title_is('Login - My Store')
            login_page = Page(browser, 'Login')
            my_account_page = login(login_page, data['user'], data['password'])
        else:
            raise AssertionError('No data available for site')
        return browser, my_account_page


def login(page, user, password):
    page.wait_element_is_visible('Email address')
    page.write('Email address', user)
    page.write('Password', password)
    page.click('Sign in')
    page.wait_title_is('My account - My Store')
    my_account_page = Page(page.browser, 'My Account')
    return my_account_page
