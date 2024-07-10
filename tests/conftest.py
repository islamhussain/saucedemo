import pytest

from tests.utils.data_loader import load_test_data, get_config_value, load_config
from tests.utils.logger import get_logger
from tests.utils.webdriver_setup import get_driver

logger = get_logger()


@pytest.fixture(scope='session')
def test_data(request):
    data_file = request.config.getoption("--data-file")
    if not data_file:
        data_file = "test_data/test_data.json"
    return load_test_data(data_file)


@pytest.fixture(scope='module')
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver = get_driver(browser, headless)
    yield driver
    driver.quit()


config = load_config("config/config.yaml")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=get_config_value('browser', config['default']['browser']))
    parser.addoption("--tags", action="store", default=get_config_value('tags', config['default']['tags']))
    parser.addoption("--headless", action="store_true", default=False, help="Run tests in headless mode")
    parser.addoption("--data-file", action="store", default=None, help="Path to the test data file")


def filter_test_cases(test_data, category, tags):
    if tags != "all":
        tag_list = tags.split(',')
        return [test for test in test_data['tests'] if
                test['category'] == category and any(tag in test['tags'] for tag in tag_list)]
    return [test for test in test_data['tests'] if test['category'] == category]


@pytest.fixture(scope='session', autouse=True)
def reset_cache(request):
    yield
    request.config.cache.set("test_data", None)


def pytest_generate_tests(metafunc):

    if 'test_case' in metafunc.fixturenames:
        category = metafunc.cls.__name__.replace('Test', '').lower()
        tags = metafunc.config.getoption('tags')
        test_data = metafunc.config.cache.get("test_data", None)
        if not test_data:
            test_data = load_test_data(metafunc.config.getoption("--data-file") or "test_data/test_data.json")
            metafunc.config.cache.set("test_data", test_data)
        filtered_tests = filter_test_cases(test_data, category, tags)
        metafunc.parametrize("test_case", filtered_tests)


def pytest_configure(config):
    config.option.metadata = {
        'Project Name': 'Swag Labs Automation',
        'Module Name': 'Login',
        'Tester': 'Pathan'
    }



