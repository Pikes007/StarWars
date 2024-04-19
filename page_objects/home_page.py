from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.base_class import BaseClass
from page_objects.view_movie_info_page import ViewMovieInfoPage


class HomePage(BaseClass):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    thead_locator = (By.CSS_SELECTOR, "thead")
    tbody_locator = (By.CSS_SELECTOR, "tbody")

    def select_movie(self, movie_name):
        """
               Select a movie by name on the Home Page.

               Args:
                   movie_name (str): The name of the movie to select.

               Returns:
                   ViewMovieInfoPage or None: An instance of ViewMovieInfoPage if the movie info page loads successfully
                                              within the timeout, otherwise returns None.
               """
        self.click_element_by_text(movie_name)
        try:
            self.wait.until(EC.url_contains("/films"))
            return ViewMovieInfoPage(self.driver)

        except TimeoutException:
            print(f"Timeout waiting for movie info page to load after selecting '{movie_name}'")
            return None
