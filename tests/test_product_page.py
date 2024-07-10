import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action, is_displayed
from tests.utils.xpaths import XPaths
from tests.utils.xpath_util import generate_xpath
import time

logger = get_logger()


@pytest.mark.usefixtures("login")
class TestProductPage:

    def test_product_page(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        start_time = time.time()
        try:
            perform_action(driver, "wait_for_visibility", XPaths.INVENTORY_LIST, timeout=20)
        except NoSuchElementException:
            logger.error(driver.page_source)  # Log page source for debugging
            raise
        load_time = time.time() - start_time

        if 'max_load_time' in test_case:
            assert load_time <= test_case[
                'max_load_time'], f"Load time {load_time} exceeds maximum {test_case['max_load_time']}"

        assert is_displayed(driver, XPaths.INVENTORY_LIST)
        logger.info(f"Test {test_case['id']} passed")

    def test_ui_elements(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        for element in test_case['expected_result']['elements']:
            try:
                perform_action(driver, "wait_for_visibility", (By.ID, element['id']), timeout=20)
                assert is_displayed(driver, (By.ID, element['id'])) == element['visible']
            except NoSuchElementException:
                logger.error(driver.page_source)  # Log page source for debugging
                assert not element['visible'], f"Element {element['id']} should not be visible"
        logger.info(f"Test {test_case['id']} passed")

    @pytest.mark.dependency()
    def test_add_to_cart(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        try:
            product_button = generate_xpath(XPaths.PRODUCT_BUTTON, product_name=test_case['product_name'])
            perform_action(driver, "click", (By.XPATH, product_button))
        except NoSuchElementException:
            logger.error(driver.page_source)  # Log page source for debugging
            raise

        assert is_displayed(driver, XPaths.CART_BADGE)
        logger.info(f"Test {test_case['id']} passed")

    @pytest.mark.dependency(depends=["TestProductPage::test_add_to_cart"])
    def test_remove_from_cart(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        try:
            remove_button_xpath = generate_xpath(XPaths.REMOVE_PRODUCT_BUTTON, product_name=test_case['product_name'])
            perform_action(driver, "click", (By.XPATH, remove_button_xpath))
            button_text = driver.find_element(By.XPATH, remove_button_xpath).text
            assert button_text == "Add to cart"
        except NoSuchElementException:
            logger.error(driver.page_source)  # Log page source for debugging
            raise
        logger.info(f"Test {test_case['id']} passed")

    def test_inventory_list_validation(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        try:
            for item in test_case['items']:
                product_name = item['name']
                product_price = item['price']
                product_image = item['image']

                product_name_xpath = generate_xpath(XPaths.PRODUCT_NAME, product_name=product_name)
                perform_action(driver, "wait_for_visibility", (By.XPATH, product_name_xpath))

                # Scroll to the element if it's available in DOM
                product_name_element = driver.find_element(By.XPATH, product_name_xpath)
                driver.execute_script("arguments[0].scrollIntoView(true);", product_name_element)

                assert is_displayed(driver, (By.XPATH, product_name_xpath))

                price_xpath = generate_xpath(XPaths.PRODUCT_PRICE, product_name=product_name)
                price_element = driver.find_element(By.XPATH, price_xpath)
                assert price_element.text == product_price, f"Expected price {product_price}, but got {price_element.text}"

                image_xpath = generate_xpath(XPaths.PRODUCT_IMAGE, product_name=product_name, product_image=product_image)
                assert is_displayed(driver, (By.XPATH, image_xpath))
        except NoSuchElementException:
            logger.error(driver.page_source)  # Log page source for debugging
            raise
        logger.info(f"Test {test_case['id']} passed")
