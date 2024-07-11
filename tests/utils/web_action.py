from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.utils.xpath_util import generate_xpath
from tests.utils.xpaths import XPaths


def perform_action(driver, action_type, element_identifier, value=None, timeout=10):
    element_type, element_value = element_identifier
    if action_type == "send_keys":
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((element_type, element_value))).send_keys(value)
    elif action_type == "click":
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((element_type, element_value))).click()
    elif action_type == "wait_for_visibility":
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((element_type, element_value)))
    elif action_type == "get_text":
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((element_type, element_value))).text
    # Add more actions as needed
    else:
        raise ValueError(f"Unsupported action type: {action_type}")


def is_displayed(driver, locator, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
        return element.is_displayed()
    except (TimeoutException, NoSuchElementException):
        return False


def add_item_to_cart(driver, product_name):
    product_link_xpath = generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=product_name)
    perform_action(driver, "click", (By.XPATH, product_link_xpath))

    add_to_cart_button_xpath = generate_xpath(XPaths.PRODUCT_BUTTON, product_name=product_name)
    perform_action(driver, "click", (By.XPATH, add_to_cart_button_xpath))

    perform_action(driver, "click", XPaths.BACK_TO_PRODUCTS_BUTTON)


def remove_item_from_cart(driver, product_name):
    product_link_xpath = generate_xpath(XPaths.DIV_TEXT_EQUALS, product_name=product_name)
    perform_action(driver, "click", (By.XPATH, product_link_xpath))
    remove_button_xpath = generate_xpath(XPaths.PRODUCT_BUTTON, product_name=product_name)
    perform_action(driver, "click", (By.XPATH, remove_button_xpath))
