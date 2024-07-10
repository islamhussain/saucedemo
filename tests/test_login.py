import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action
import time

logger = get_logger()


class TestLogin:

    def test_login(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/")

        start_time = time.time()
        perform_action(driver, "send_keys", (By.ID, "user-name"), test_case['username'])
        perform_action(driver, "send_keys", (By.ID, "password"), test_case['password'])
        perform_action(driver, "click", (By.ID, "login-button"))
        load_time = time.time() - start_time

        if 'max_load_time' in test_case:
            assert load_time <= test_case[
                'max_load_time'], f"Load time {load_time} exceeds maximum {test_case['max_load_time']}"

        if test_case['expected_result'] == "inventory.html":
            perform_action(driver, "wait_for_visibility", (By.CSS_SELECTOR, "div.inventory_list"))
            assert "inventory.html" in driver.current_url
        else:
            perform_action(driver, "wait_for_visibility", (By.CSS_SELECTOR, test_case['expected_result']))
            assert driver.find_element(By.CSS_SELECTOR, test_case['expected_result']).is_displayed()
        logger.info(f"Test {test_case['id']} passed")


class TestUIElements:

    def test_ui_elements(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/")

        for element in test_case['expected_result']['elements']:
            try:
                perform_action(driver, "wait_for_visibility", (By.ID, element['id']))
                assert driver.find_element(By.ID, element['id']).is_displayed() == element['visible']
            except NoSuchElementException:
                assert not element['visible'], f"Element {element['id']} should not be visible"
        logger.info(f"Test {test_case['id']} passed")
