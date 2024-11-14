import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def test_cart_functionality(browser):
    """Test adding items to the cart and validating the cart content."""
    logging.info("Starting test: Cart Functionality")

    # Step 2: Add an item to the cart (e.g., Samsung Galaxy S6)
    product_link = wait_for_clickable(browser, By.LINK_TEXT, "Samsung galaxy s6")
    product_link.click()

    # Wait for product page to load
    wait_for_element(browser, By.CLASS_NAME, "name")

    # Step 3: Click 'Add to Cart' button
    add_to_cart_button = wait_for_clickable(browser, By.XPATH, "//a[text()='Add to cart']")
    add_to_cart_button.click()

    # Step 4: Handle alert confirming addition to the cart
    try:
        alert = WebDriverWait(browser, 5).until(EC.alert_is_present())
        assert "Product added" in alert.text, f"Unexpected alert message: {alert.text}"
        alert.accept()
        logging.info("Product successfully added to the cart.")
    except TimeoutException:
        logging.error("No alert appeared after adding product to the cart.")
        raise

    # Step 5: Navigate to the Cart page
    cart_link = wait_for_clickable(browser, By.ID, "cartur")
    cart_link.click()

    # Step 6: Validate the product is in the cart
    try:
        product_in_cart = wait_for_element(browser, By.XPATH, "//td[text()='Samsung galaxy s6']")
        assert product_in_cart is not None, "Product not found in the cart"
        logging.info("Product is present in the cart.")
    except TimeoutException:
        logging.error("Product was not found in the cart.")
        raise

    # Step 7: Delete the product from the cart
    delete_button = wait_for_clickable(browser, By.XPATH, "//a[text()='Delete']")
    delete_button.click()
    time.sleep(2)  # Give some time for the deletion to take effect

    # Step 8: Verify the cart is empty
    try:
        empty_cart_message = wait_for_element(browser, By.XPATH, "//h3[@id='totalp']")
        assert "" in empty_cart_message.text, "Cart is empty after deletion"
        logging.info("Test passed: Product was successfully deleted from the cart.")
    except AssertionError:
        logging.error("Cart still contains items after deletion.")
        raise
