import pytest
from selenium.webdriver.common.by import By

from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action, is_displayed
from tests.utils.xpaths import XPaths
from tests.utils.xpath_util import generate_xpath

logger = get_logger()


@pytest.mark.usefixtures("login")
class TestEndToEnd:

    def test_end_to_end(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        # Add product to cart
        product_button = generate_xpath(XPaths.PRODUCT_BUTTON, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, product_button))
        assert is_displayed(driver, XPaths.CART_BADGE)

        # Go to cart
        perform_action(driver, "click", (By.CSS_SELECTOR, "a.shopping_cart_link"))

        # Verify product in cart
        assert is_displayed(driver, (By.XPATH, f"//div[text()='{test_case['product_name']}']"))

        # Checkout
        perform_action(driver, "click", (By.ID, "checkout"))
        perform_action(driver, "send_keys", (By.ID, "first-name"), test_case['first_name'])
        perform_action(driver, "send_keys", (By.ID, "last-name"), test_case['last_name'])
        perform_action(driver, "send_keys", (By.ID, "postal-code"), test_case['postal_code'])
        perform_action(driver, "click", (By.ID, "continue"))
        perform_action(driver, "click", (By.ID, "finish"))

        # Verify checkout complete
        assert is_displayed(driver, (By.CSS_SELECTOR, "h2.complete-header"))
        logger.info(f"Test {test_case['id']} passed")
