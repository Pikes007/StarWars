import pandas as pd
from utilities.base_class import BaseClass


class TestApi(BaseClass):

    def test_get_movie_count(self):
        """
                Test the total count of movies returned by the API.

                Raises:
                    AssertionError: If the count of movies is not as expected (6).
                """
        data = self.api_movie_search()
        assert data["count"] == 6
        print("Movie count == 6")

    def test_get_movie3(self):
        """
                Test the director of the third movie returned by the API.

                Raises:
                    AssertionError: If the director of the third movie is not 'Richard Marquand'.
                """
        data = self.api_movie_search()
        assert data["results"][2]["director"] == "Richard Marquand"
        print(f'The director of {data["results"][2]["title"]} = {data["results"][2]["director"]}')

    def test_get_movie5(self):
        """
                Test the producer of the fifth movie returned by the API.

                Raises:
                    AssertionError: If the producer of the fifth movie is 'Gary Kutz, George Lucas'.
                """
        data = self.api_movie_search()
        assert data["results"][4]["producer"] != "Gary Kutz, George Lucas"
        print(f'The producer of {data["results"][4]["title"]} = {data["results"][4]["producer"]}')

    def test_bonus_make_dataframe(self):
        """
                Test creation of a DataFrame from movie data returned by the API.

                - Extracts movie titles, producers, and directors from the API response.
                - Creates a DataFrame using extracted data and adds 1-based indexing to DataFrame rows.
                - Prints the resulting DataFrame.

                Note:
                    This test does not perform assertions but demonstrates DataFrame creation from API data.
                """
        data = self.api_movie_search()
        titles = []
        producers = []
        directors = []
        for movie in data["results"]:
            title = movie["title"]
            producer = movie["producer"]
            director = movie["director"]

            titles.append(title)
            producers.append(producer)
            directors.append(director)

        movie_df = pd.DataFrame({
            "Title": titles,
            "Producer": producers,
            "Director": directors
            })
        movie_df.index = movie_df.index + 1
        print(movie_df)

