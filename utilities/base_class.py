import json

import pandas as pd
import pytest
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import BASE_URI


@pytest.mark.usefixtures("setup")
class BaseClass:

    def scrape_table_data(self, headers_locator, body_locator, header_tag='th', row_tag='tr', cell_tag='td'):
        """
                Scrape data from an HTML table on the current page.

                Args:
                    headers_locator (tuple): Locator for the table headers.
                    body_locator (tuple): Locator for the table body.
                    header_tag (str, optional): HTML tag for table headers (default is 'th').
                    row_tag (str, optional): HTML tag for table rows (default is 'tr').
                    cell_tag (str, optional): HTML tag for table cells (default is 'td').

                Returns:
                    pd.DataFrame: A pandas DataFrame containing the scraped table data.
                """
        headers_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(headers_locator)
        )
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table_data = []
        headers = [i.text.strip() for i in soup.find(headers_locator).find_all(header_tag)]

        body_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(body_locator)
        )

        for row in soup.find(body_locator).find_all(row_tag):
            columns = row.find_all(cell_tag)
            row_data = {}
            for idx, column in enumerate(columns):
                row_data[headers[idx]] = column.text.strip()
            table_data.append(row_data)

        df = pd.DataFrame(table_data)
        df.index = df.index + 1
        return df

    def click_element_by_text(self, text):
        """
                Click on an element identified by its visible text.

                Args:
                    text (str): The visible text of the element to click.
                """
        try:
            text_xpath = f"//a[normalize-space()='{text}']"
            target_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, text_xpath))
            )
            target_element.click()
        except NoSuchElementException as e:
            print(f"'{text}' was not found", str(e))

    def scroll_into_view(self, css_locator):
        """
                Scroll the page to bring a specific element into view.

                Args:
                    css_locator (str): CSS locator of the element to scroll into view.
                """
        element = self.driver.find_element(By.CSS_SELECTOR, css_locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def api_movie_search(self):
        """
                Perform a movie search API request.

                Returns:
                    dict: JSON response containing movie search results.
                """
        response = self.api_session.get(BASE_URI + f"films")
        data = json.loads(response.text)
        assert response.status_code == 200, f"Expected status code, but received {response.status_code}"
        return data
