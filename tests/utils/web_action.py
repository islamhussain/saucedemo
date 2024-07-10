from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
