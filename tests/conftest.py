import pytest
import requests
from selenium import webdriver

BASE_URI = "https://swapi.dev/api/"


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def setup(request, api_session):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = None
    if "web" in request.keywords:
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        url = "http://localhost:3000"
        driver.get(url)
        driver.maximize_window()
    request.cls.driver = driver
    request.cls.api_session = api_session

    yield driver

    if request.cls.driver:
        driver.close()
