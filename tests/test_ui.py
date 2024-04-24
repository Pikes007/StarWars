import pytest
from utilities.base_class import BaseClass
from page_objects.home_page import HomePage


@pytest.mark.web
class TestInterface(BaseClass):

    def test_sort_movies(self):
        """
                Test sorting of movies on the Home Page.

                - Retrieves movie data from the Home Page.
                - Sorts the movie data by title.
                - Verifies that 'The Phantom Menace' is the last movie in the sorted list.

                Raises:
                    AssertionError: If the expected movie is not found as the last entry in the sorted list.
                """
        homepage = HomePage(self.driver)
        home_data = self.soup_scrape(parent_header_tag="thead", parent_body_tag="tbody", header_tag="th", row_tag="tr", cell_tag="td",equal_length_column = True)
        sorted_home_data = home_data.sort_values(by="Title")
        assert sorted_home_data.iloc[-1]["Title"] == "The Phantom Menace"
        print("Movie at row index -1 = The Phantom Menace")
        print(home_data)
        print(sorted_home_data)

    def test_view_movie_check_species(self):
        """
                Test species information for a specific movie.

                - Selects a movie ('The Empire Strikes Back') from the Home Page.
                - Scrolls to the movie's layout on the page.
                - Retrieves and processes movie information.
                - Verifies if 'Wookie' species is listed in the movie's species information.

                Raises:
                    AssertionError: If 'Wookie' species is not found in the movie's species information.
                """
        homepage = HomePage(self.driver)
        view_movie = homepage.select_movie("The Empire Strikes Back")
        self.scroll_into_view(view_movie.layout_class)
        movie_data = self.soup_scrape(parent_header_tag="main", parent_body_tag="main", header_tag="h1", row_tag="ul", cell_tag="li", equal_length_column = False)
        assert "Wookie" in movie_data["Species"].values, "Wookie species should be in the movie's species."
        print("Wookie is listed in Species information")
        print(movie_data)

    def test_check_planets(self):
        """
                Test planet information for a specific movie.

                - Selects a movie ('The Phantom Menace') from the Home Page.
                - Scrolls to the movie's layout on the page.
                - Retrieves and processes movie information.
                - Verifies if 'Camino' planet is not listed in the movie's planets information.

                Raises:
                    AssertionError: If 'Camino' planet is found in the movie's planets information.
                """
        homepage = HomePage(self.driver)
        view_movie = homepage.select_movie("The Phantom Menace")
        self.scroll_into_view(view_movie.layout_class)
        movie_data = self.soup_scrape(parent_header_tag="main", parent_body_tag="main", header_tag="h1", row_tag="ul", cell_tag="li", equal_length_column = False)
        assert "Camino" not in movie_data["Planets"].values, "Camino should not be listed under planets for this movie"
        print("Camino is not listed as a planet for this movie")
        print(movie_data)

