import pytest
from selenium.webdriver.common.by import By
from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action, is_displayed
from tests.utils.xpaths import XPaths
from tests.utils.xpath_util import generate_xpath

logger = get_logger()


@pytest.mark.usefixtures("login")
class TestItemPage:

    def test_view_product_details(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        product_link_xpath = generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, product_link_xpath))

        assert is_displayed(driver, (By.XPATH, f"//div[text()='{test_case['expected_result']['name']}']"))
        price_element = driver.find_element(By.XPATH, generate_xpath(XPaths.DIV_CLASS_EQUALS,
                                                                     css=test_case['price_css']))
        assert price_element.text == test_case['expected_result']['price']
        assert is_displayed(driver, (By.XPATH, f"//div[text()='{test_case['expected_result']['description']}']"))

        logger.info(f"Test {test_case['id']} passed")

    def test_add_item_to_cart(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        product_link_xpath = generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, product_link_xpath))

        add_to_cart_button_xpath = generate_xpath(XPaths.PRODUCT_BUTTON, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, add_to_cart_button_xpath))

        assert is_displayed(driver, XPaths.CART_BADGE)
        logger.info(f"Test {test_case['id']} passed")

    def test_remove_item_from_cart(self, driver, test_case, reset_app_state):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        product_link_xpath = generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, product_link_xpath))

        add_to_cart_button_xpath = generate_xpath(XPaths.PRODUCT_BUTTON, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, add_to_cart_button_xpath))

        remove_button_xpath = generate_xpath(XPaths.REMOVE_PRODUCT_BUTTON, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, remove_button_xpath))

        button_text = driver.find_element(By.XPATH, remove_button_xpath).text
        assert button_text == "Add to cart"

        logger.info(f"Test {test_case['id']} passed")

    def test_back_to_products(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        product_link_xpath = generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, product_link_xpath))

        perform_action(driver, "click", XPaths.BACK_TO_PRODUCTS_BUTTON)

        assert "inventory.html" in driver.current_url
        logger.info(f"Test {test_case['id']} passed")
