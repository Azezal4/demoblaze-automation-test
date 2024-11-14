import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException, 
)

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Ensure logs are printed to console
)

def wait_for_element(browser, by, value, timeout=10):
    """Utility function for explicit waits."""
    return WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, value)))

def wait_for_clickable(browser, by, value, timeout=10):
    """Utility function for waiting until an element is clickable."""
    return WebDriverWait(browser, timeout).until(EC.element_to_be_clickable((by, value)))


# chrome_options.add_argument("--headless")  # Uncomment for headless mode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Example test with explicit waits
def test_home_page_title(browser):
    logging.info("Starting test: Home Page Title")
    assert "STORE" in browser.title, "Title mismatch"
    logging.info("Test passed: Home Page Title")

@pytest.mark.parametrize("username, password, expected", [
    ("ujjwal101", "Hello@123", True),
    ("ujjwal10", "Hel", True),
    ("hello", "jejej", True),
    ("Adam", "102252", True),
    ("Leo", "102252", False),
    ("Laos", "90909", False),
])

def test_login_functionality(browser, username, password, expected):
    logging.info(f"Starting test: Login Functionality with user '{username}'")

    login_button = wait_for_clickable(browser, By.ID, "login2")
    login_button.click()

    # Wait until the login modal appears
    wait_for_element(browser, By.ID, "logInModal")

    username_input = browser.find_element(By.ID, "loginusername")
    password_input = browser.find_element(By.ID, "loginpassword")

    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    submit_button = browser.find_element(By.XPATH, "//button[text()='Log in']")
    submit_button.click()
    try:
        if expected:
            # Wait for the logout button to confirm successful login
            wait_for_element(browser, By.ID, "logout2")
            assert "Log out" in browser.page_source, "Login failed with valid credentials"
            logging.info("Test passed: Login Functionality with valid credentials")
        else:
            # Handle the alert and check its message for failed login
            alert = WebDriverWait(browser, 5).until(EC.alert_is_present())
            alert_text = alert.text
            assert alert_text in ["User does not exist.", "Wrong password."], f"Unexpected alert text: {alert_text}"
            alert.accept()
            logging.info(f"Test passed: Login Functionality - Handled alert with message '{alert_text}'")
    except TimeoutException:
        logging.error("Test failed: Login functionality - No expected alert or logout button found.")
        raise
    except AssertionError as e:
        logging.error(f"Test failed: {str(e)}")
        raise


if __name__ == "__main__":
    pytest.main()
