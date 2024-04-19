import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utilities.base_class import BaseClass


class ViewMovieInfoPage(BaseClass):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    layout_class = ".layout_lists__rBjPn"
    body_class = (By.CSS_SELECTOR, ".border-2")
    info_headings_locator = (By.CSS_SELECTOR, "main")

    def get_movie_info(self):
        """
                Extract basic movie information from the page.

                Returns:
                    pd.Series: A pandas Series containing extracted movie information.
                """
        data_list = []
        movie_info = self.driver.find_elements(*ViewMovieInfoPage.body_class)
        for item in movie_info:
            item_text = item.text
            parts = item_text.split("\n")
            data_list.append(parts[0])
        data_ser = pd.Series(data_list)
        return data_ser

    def split_series_by_labels(self, series):
        """
                Split a pandas Series into DataFrame based on predefined section labels.

                Args:
                    series (pd.Series): The pandas Series to process.

                Returns:
                    pd.DataFrame: A DataFrame containing data organized by predefined section labels.
                """
        data_dict = {}
        section_labels = ['Characters', 'Planets', 'Species', 'Starships', 'Vehicles']

        for label in section_labels:
            data_dict[label] = []

        current_label = None
        for item in series:
            if item in section_labels:
                current_label = item
            elif current_label is not None:
                data_dict[current_label].append(item)

        df = pd.DataFrame.from_dict(data_dict, orient="index").transpose()
        return df
