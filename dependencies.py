from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
