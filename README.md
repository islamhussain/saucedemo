### README.md

# Swag Labs Automation Framework

## Introduction
This framework is designed for automated testing of the Swag Labs application using Selenium WebDriver with PyTest. It supports data-driven testing, cross-browser testing, headless mode, and detailed reporting.

## Setup Instructions

### Prerequisites
1. Python 3.7 or above
2. Google Chrome, Mozilla Firefox, or Microsoft Edge

### Installation

1. **Clone the repository:**
   ```bash
   https://github.com/islamhussain/saucedemo.git
   cd saucedemo
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

1. **Run all tests:**
   ```bash
   pytest --browser=chrome --headless --tags=all --test_data=tests/test_data
   ```

2. **Run specific tests:**
   ```bash
   pytest tests/test_product_page.py --browser=firefox --tags=smoke --test_data=tests/test_data/product_page.json
   ```

3. **Generate HTML report:**
   ```bash
   cd tests
   pytest --html=reports/report.html
   ```

### Running Tests with Custom Test Data
To run tests using custom test data, provide either the directory path or the JSON file path of the test data:

```bash
cd tests
# Using a directory of test data files
pytest --test_data_dir=/path/to/custom/test_data/

# Using a single test data file
pytest --test_data_file=/path/to/custom/test_data.json
```

## Framework Structure

### Directory Structure

```
|-- tests
|   |-- config
|   |   |-- config.yaml
|   |-- reports
|   |   |-- assets
|   |       |-- report.html
|   |-- test_data
|   |   |-- end_to_end.json
|   |   |-- product_page.json
|   |   |-- test_data.json
|   |-- utils
|   |   |-- data_loader.py
|   |   |-- data_merger.py
|   |   |-- logger.py
|   |   |-- web_action.py
|   |   |-- webdriver_setup.py
|   |   |-- xpath_util.py
|   |   |-- xpaths.py
|   |-- conftest.py
|   |-- test_checkout.py
|   |-- test_end_to_end.py
|   |-- test_login.py
|   |-- test_logout.py
|   |-- test_negative.py
|   |-- test_product_page.py
|   |-- test_shopping_cart.py
|-- requirements.txt
```

### Configuration Files

- **config.yaml**: Contains default configurations like browser, tags, and test data directory.

### Utilities

- **data_loader.py**: Functions to load test data from JSON files.
- **data_merger.py**: Merges multiple test data JSON files from a directory or single file.
- **logger.py**: Configures and provides logging functionality.
- **web_action.py**: Contains reusable functions for web interactions like clicking, sending keys, etc.
- **webdriver_setup.py**: Manages WebDriver setup for different browsers and headless mode using WebDriver managers.
- **xpath_util.py**: Utility to generate dynamic XPaths.
- **xpaths.py**: Stores common XPaths used in the tests.

### Sample Test Data (test_data.json)
```json
{
    "tests": [
        {
            "id": "L001",
            "description": "Login with valid credentials",
            "category": "login",
            "tags": ["smoke", "positive"],
            "username": "standard_user",
            "password": "secret_sauce",
            "expected_result": "inventory.html"
        }
    ]
}
```

### Sample Test Script (test_login.py)
```python
import pytest
from selenium.webdriver.common.by import By
from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action
from tests.utils.xpaths import XPaths

logger = get_logger()

@pytest.mark.usefixtures("login")
class TestLogin:
    
    def test_login(self, driver, test_case):
        logger.info(f"Executing test: {test_case['description']} with ID: {test_case['id']}")
        driver.get("https://www.saucedemo.com/")
        
        perform_action(driver, "send_keys", XPaths.USERNAME_FIELD, test_case['username'])
        perform_action(driver, "send_keys", XPaths.PASSWORD_FIELD, test_case['password'])
        perform_action(driver, "click", XPaths.LOGIN_BUTTON)
        
        if test_case['expected_result'] == "inventory.html":
            perform_action(driver, "wait_for_visibility", XPaths.INVENTORY_LIST)
            assert "inventory.html" in driver.current_url
        else:
            assert False, "Login test failed"
        logger.info(f"Test {test_case['id']} passed")
```

#### Future Scope
1. Enabling multi threading over test classes
2. Low code solution and more data driven 
3. Add CI/CD and DockerFile

This README provides a comprehensive guide to setting up, configuring, and running tests with the Swag Labs Automation Framework.
