from business.page import Page


def search_product(page, product):
    page.write('Search', product)
    page.press_key('Search', 'ENTER')
    return Page(page.browser, 'Search')


def add_to_cart(page, product):
    product_xpath = "//a[@class='product-name' and @title='{product_name}']".format(product_name=product)
    page.hover(element_name=None, xpath=product_xpath)
    page.wait_element_is_clickable('Add to cart')
    page.click('Add to cart')
    cart_dialog = Page(page.browser, 'Cart Dialog')
    cart_dialog.wait_element_is_clickable('Proceed to checkout')
    cart_dialog.click('Proceed to checkout')
    cart_page = Page(page.browser, 'Cart')
    return cart_page


def is_product_in_cart(table, product_name):
    return table.data_in_column_exists(product_name, 'Description')


def get_product_quantity(table, product_name):
    cell_quantity = 0
    table_rows = table.get_rows()
    for row in table_rows:
        cell_text = table.get_cell_column_text(row, 'Description')
        if cell_text == product_name:
            cell_quantity = table.get_cell_column_text(row, 'Qty')
            break

    return int(cell_quantity)
