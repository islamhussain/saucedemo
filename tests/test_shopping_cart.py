import pytest
from selenium.webdriver.common.by import By
from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action, is_displayed, add_item_to_cart, remove_item_from_cart
from tests.utils.xpaths import XPaths
from tests.utils.xpath_util import generate_xpath

logger = get_logger()


@pytest.mark.usefixtures("login")
class TestShoppingCart:

    def test_verify_product_details(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        add_item_to_cart(driver, test_case['product_name'])

        perform_action(driver, "click", XPaths.CART_BADGE)

        assert is_displayed(driver, (
            By.XPATH, generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=test_case['expected_result']['name'])))
        price_element = driver.find_element(By.XPATH, generate_xpath(XPaths.PRODUCT_PRICE_IN_CHECKOUT,
                                                                     product_name=test_case['expected_result']['name']))
        assert price_element.text == test_case['expected_result']['price']
        logger.info(f"Test {test_case['id']} passed")

    def test_remove_item_from_cart(self, driver, test_case, reset_app_state):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        add_item_to_cart(driver, test_case['product_name'])

        perform_action(driver, "click", XPaths.CART_BADGE)

        remove_button_xpath = generate_xpath(XPaths.PRODUCT_BUTTON_IN_CHECKOUT, product_name=test_case['product_name'])
        perform_action(driver, "click", (By.XPATH, remove_button_xpath))

        # Verify the cart is empty
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0, "Cart is not empty after removing the item"

        logger.info(f"Test {test_case['id']} passed")

    def test_add_multiple_items(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        for product in test_case['products']:
            add_item_to_cart(driver, product['name'])

        perform_action(driver, "click", XPaths.CART_BADGE)

        for product in test_case['products']:
            assert is_displayed(driver,
                                (By.XPATH, generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=product['name'])))
            price_element = driver.find_element(By.XPATH,
                                                generate_xpath(XPaths.PRODUCT_PRICE_IN_CHECKOUT, product_name=product['name']))
            assert price_element.text == product['price']

        logger.info(f"Test {test_case['id']} passed")

    def test_navigate_to_checkout(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/inventory.html")

        for product in test_case['products']:
            add_item_to_cart(driver, product['name'])

        perform_action(driver, "click", XPaths.CART_BADGE)
        perform_action(driver, "click", XPaths.CHECKOUT_BUTTON)

        assert "checkout-step-one.html" in driver.current_url
        logger.info(f"Test {test_case['id']} passed")

    @pytest.mark.xfail(reason="No error is thrown on empty cart checkout")
    def test_empty_cart_checkout(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/cart.html")

        perform_action(driver, "click", XPaths.CHECKOUT_BUTTON)

        error_message_xpath = generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name="Error: No items in your cart.")
        assert is_displayed(driver, (By.XPATH, error_message_xpath))

        logger.info(f"Test {test_case['id']} passed")

    def test_different_user_carts(self, driver, test_case, reset_app_state):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")

        # User 1: Add items to cart

        for product in test_case['products_user1']:
            add_item_to_cart(driver, product['name'])

        perform_action(driver, "click", XPaths.BURGER_MENU_BUTTON)
        perform_action(driver, "click", XPaths.LOGOUT_SIDEBAR_LINK)

        # User 2: Add different items to cart
        perform_action(driver, "send_keys", XPaths.USERNAME_FIELD, test_case['username_user2'])
        perform_action(driver, "send_keys", XPaths.PASSWORD_FIELD, test_case['password_user2'])
        perform_action(driver, "click", XPaths.LOGIN_BUTTON)

        for product in test_case['products_user2']:
            add_item_to_cart(driver, product['name'])

        perform_action(driver, "click", XPaths.CART_BADGE)

        for product in test_case['products_user2']:
            assert is_displayed(driver,
                                (By.XPATH, generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=product['name'])))

        logger.info(f"Test {test_case['id']} passed")
