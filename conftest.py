
import pytest
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


CHROME_DRIVER_PATH = "C:/Users/uazez/OneDrive/Documents/Capstone Project/chromedriver-win64/chromedriver.exe"
# Set up Chrome WebDriver options
chrome_options = Options()
@pytest.fixture
def browser():
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)  # Set an implicit wait for all elements
    driver.get("https://www.demoblaze.com/")
    yield driver
    driver.quit()