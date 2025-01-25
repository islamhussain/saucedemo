import os

import pytest

from tests.utils.data_loader import load_test_data, get_config_value, load_config
from tests.utils.data_merger import merge_test_data
from tests.utils.logger import get_logger
from tests.utils.web_action import perform_action
from tests.utils.webdriver_setup import get_driver
from tests.utils.xpaths import XPaths

logger = get_logger()


def resolve_test_data(obj):
    test_data_path = obj.config.getoption("--test_data")
    if os.path.isdir(test_data_path):
        test_data = merge_test_data(directory=test_data_path)
    else:
        test_data = merge_test_data(file_path=test_data_path)
    return test_data


@pytest.fixture(scope='session')
def test_data(request):
    resolve_test_data(request)


@pytest.fixture(scope='module')
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver = get_driver(browser, headless)
    yield driver
    driver.quit()


config = load_config("tests/config/config.yaml")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=get_config_value('browser', config['default']['browser']))
    parser.addoption("--tags", action="store", default=get_config_value('tags', config['default']['tags']))
    parser.addoption("--headless", action="store_true", default=False, help="Run tests in headless mode")
    parser.addoption("--test_data", action="store", default=None, help="Directory containing test data JSON files")


def filter_test_cases(test_data, tags):
    if tags != "all":
        tag_list = tags.split(',')
        return [test for test in test_data['tests'] if any(tag in test['tags'] for tag in tag_list)]
    return test_data['tests']


def pytest_generate_tests(metafunc):
    if 'test_case' in metafunc.fixturenames:
        test_data = resolve_test_data(metafunc)
        tags = metafunc.config.getoption('tags')
        filtered_tests = filter_test_cases(test_data, tags)
        function_name = metafunc.function.__name__.replace('test_', '')
        category_tests = [test for test in filtered_tests if test['category'] == function_name]
        metafunc.parametrize("test_case", category_tests, ids=[tc['id'] for tc in category_tests])


@pytest.fixture
def reset_app_state(login, driver):
    perform_action(driver, "click", XPaths.BURGER_MENU_BUTTON)
    perform_action(driver, "click", XPaths.RESET_APP_STATE)


@pytest.fixture(scope='class', autouse=True)
def reset_app_state_class(driver):
    username = 'standard_user'
    password = 'secret_sauce'

    driver.get("https://www.saucedemo.com/")
    perform_action(driver, "send_keys", XPaths.USERNAME_FIELD, username)
    perform_action(driver, "send_keys", XPaths.PASSWORD_FIELD, password)
    perform_action(driver, "click", XPaths.LOGIN_BUTTON)
    perform_action(driver, "click", XPaths.BURGER_MENU_BUTTON)
    perform_action(driver, "click", XPaths.RESET_APP_STATE)
    perform_action(driver, "click", XPaths.LOGOUT_SIDEBAR_LINK)


@pytest.fixture(scope='function')
def login(driver, test_case):
    username = test_case.get('username', 'standard_user')
    password = test_case.get('password', 'secret_sauce')

    driver.get("https://www.saucedemo.com/")
    perform_action(driver, "send_keys", XPaths.USERNAME_FIELD, username)
    perform_action(driver, "send_keys", XPaths.PASSWORD_FIELD, password)
    perform_action(driver, "click", XPaths.LOGIN_BUTTON)
    yield
    try:
        perform_action(driver, "click", XPaths.BURGER_MENU_BUTTON)
        perform_action(driver, "click", XPaths.LOGOUT_SIDEBAR_LINK)
    except:
        pass


def pytest_configure(config):
    config.option.metadata = {
        'Project Name': 'Swag Labs Automation',
        'Tester': 'Pathan'
    }



