import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action, is_displayed
from tests.utils.xpaths import XPaths
import time

logger = get_logger()


class TestLogin:

    def test_login(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/")

        start_time = time.time()
        perform_action(driver, "send_keys", XPaths.USERNAME_FIELD, test_case['username'])
        perform_action(driver, "send_keys", XPaths.PASSWORD_FIELD, test_case['password'])
        perform_action(driver, "click", XPaths.LOGIN_BUTTON)
        load_time = time.time() - start_time

        if 'max_load_time' in test_case:
            assert load_time <= test_case['max_load_time'], f"Load time {load_time} exceeds maximum {test_case['max_load_time']}"

        if test_case['expected_result'] == "inventory.html":
            perform_action(driver, "wait_for_visibility", XPaths.INVENTORY_LIST)
            assert "inventory.html" in driver.current_url
        else:
            perform_action(driver, "wait_for_visibility", (By.CSS_SELECTOR, test_case['expected_result']))
            assert is_displayed(driver, (By.CSS_SELECTOR, test_case['expected_result']))
        logger.info(f"Test {test_case['id']} passed")

    def test_ui_elements(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/")

        for element in test_case['expected_result']['elements']:
            try:
                perform_action(driver, "wait_for_visibility", (By.ID, element['id']), timeout=20)
                assert is_displayed(driver, (By.ID, element['id'])) == element['visible']
            except NoSuchElementException:
                logger.error(driver.page_source)  # Log page source for debugging
                assert not element['visible'], f"Element {element['id']} should not be visible"
        logger.info(f"Test {test_case['id']} passed")
