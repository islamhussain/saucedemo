import pytest
from selenium.webdriver.common.by import By
from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action, is_displayed
from tests.utils.xpaths import XPaths
from tests.utils.xpath_util import generate_xpath

logger = get_logger()


@pytest.mark.usefixtures("login")
class TestCheckoutPage:

    def checkout(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        perform_action(driver, "click",
                       (By.XPATH, generate_xpath(XPaths.PRODUCT_BUTTON, product_name="Sauce Labs Backpack")))
        perform_action(driver, "click", XPaths.CART_BADGE)

        if test_case['description'] == "Cancel checkout":
            perform_action(driver, "click", XPaths.CHECKOUT_BUTTON)
            perform_action(driver, "click", XPaths.CANCEL_BUTTON)
            assert "cart.html" in driver.current_url
        else:
            perform_action(driver, "click", XPaths.CHECKOUT_BUTTON)
            perform_action(driver, "send_keys", XPaths.FIRST_NAME_FIELD, test_case['first_name'])
            perform_action(driver, "send_keys", XPaths.LAST_NAME_FIELD, test_case['last_name'])
            perform_action(driver, "send_keys", XPaths.ZIP_CODE_FIELD, test_case['postal_code'])
            perform_action(driver, "click", XPaths.CONTINUE_BUTTON)

            if "Error" in test_case['expected_result']:
                error_message = driver.find_element(*XPaths.ERROR_MESSAGE).text
                assert error_message == test_case['expected_result']
            else:
                assert test_case['expected_result'] in driver.current_url

        logger.info(f"Test {test_case['id']} passed")

    def test_cancel_checkout(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/checkout-step-one.html")

        perform_action(driver, "click", XPaths.CANCEL_BUTTON)

        assert "cart.html" in driver.current_url
        logger.info(f"Test {test_case['id']} passed")

    def test_checkout_cases(self, driver, test_case, reset_app_state):
        if test_case.get('xfail', False):
            pytest.xfail("Expected failure due to fuzzy data")
        self.checkout(driver, test_case)
