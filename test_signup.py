import time
import pytest
from selenium.webdriver.common.by import By

@pytest.mark.parametrize("username, password, expected", [
    ("hero", "1234", False),
])

def test_signup(browser, username, password, expected):
    # Locate and click the Sign up button
    signup_button = browser.find_element(By.ID, "signin2")
    signup_button.click()

    # Wait for the signup modal to appear
    time.sleep(2)  # Consider using WebDriverWait for better performance

    # Locate the username and password fields in the modal
    username_field = browser.find_element(By.ID, "sign-username")
    password_field = browser.find_element(By.ID, "sign-password")

    # Fill out the form
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)

    # Click on the sign-up button in the modal
    modal_signup_button = browser.find_element(By.XPATH, "//button[text()='Sign up']")
    modal_signup_button.click()

    time.sleep(5)  

    try:
        alert = browser.switch_to.alert
        alert_message = alert.text
        alert.accept()
        assert "Sign up successful." in alert_message  # Check expected message
    except:
        pytest.fail("No alert or unexpected alert message")
