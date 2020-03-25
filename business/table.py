

class Table:
    def __init__(self, browser, table_name, xpath_def):
        self._browser = browser
        self._table_name = table_name
        self._xpath_def = xpath_def

    def get_rows(self):
        rows = self._browser.driver.find_elements_by_xpath(self._xpath_def['rows'])
        return rows

    def data_in_column_exists(self, value, column_name):
        exists = False
        rows = self._browser.driver.find_elements_by_xpath(self._xpath_def['rows'])
        for row in rows:
            cell_text = self.get_cell_column_text(row, column_name)
            if value == cell_text:
                exists = True
                break

        return exists

    def get_cell_column_text(self, row, column_name):
        cell = row.find_element_by_xpath(self._xpath_def['Columns'].get(column_name, None))
        value = None
        if cell.text:
            value = cell.text
        elif cell.get_attribute('value'):
            value = cell.get_attribute('value')
        return value
