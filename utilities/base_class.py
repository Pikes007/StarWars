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

    def soup_scrape(self, parent_header_tag=None, parent_body_tag=None, header_tag=None, row_tag=None,
                    cell_tag=None,
                    equal_length_column=False):
        """
            Scrape data from a webpage using BeautifulSoup.

            Args:
                parent_header_tag (str, optional): Tag name of the parent element containing the header.
                parent_body_tag (str, optional): Tag name of the parent element containing the body.
                header_tag (str, optional): Tag name of individual header elements.
                row_tag (str, optional): Tag name of individual row elements.
                cell_tag (str, optional): Tag name of individual cell elements.
                equal_length_column (bool, optional): If True, create DataFrame directly from body data.

            Returns:
                pandas.DataFrame: DataFrame containing scraped data.

            Raises:
                TimeoutException: If the specified header element is not found within the timeout (10 seconds).
            """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, header_tag))
        )
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        headers = [i.text.strip() for i in soup.find(parent_header_tag).find_all(header_tag)]
        bodies = [
            [cell.text.strip() for cell in row.find_all(cell_tag)]
            for row in soup.find(parent_body_tag).find_all(row_tag)
        ]
        if equal_length_column:
            df = pd.DataFrame(bodies, columns=headers)
        else:
            data_dict = {header: body for header, body in zip(headers, bodies)}
            df = pd.DataFrame.from_dict(data_dict, orient="index").transpose()

        df.index = df.index + 1
        return df
