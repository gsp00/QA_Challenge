import pytest
from tests.steps.login import *
from tests.steps.products import *


@pytest.fixture()
def initial_page():
    browser, my_account_page = open_site_and_login()
    yield my_account_page
    browser.stop()


def test_demo(initial_page):
    search_page = search_product(initial_page, 'Blouse')
    cart_page = add_to_cart(search_page, 'Blouse')
    cart_table = cart_page.get_table('Cart Table')

    fail_msg = 'Product {} was not found in table'.format('Blouse')
    assert is_product_in_cart(cart_table, 'Blouse'), fail_msg

    qty_expected = 1
    qty_found = get_product_quantity(cart_table, 'Blouse')
    fail_msg = 'Qty of product {product_name} is not correct - Expected {qty_expected} - Found {qty_found}'\
        .format(product_name='Blouse', qty_expected=qty_expected, qty_found=qty_found)
    assert qty_found == qty_expected, fail_msg











