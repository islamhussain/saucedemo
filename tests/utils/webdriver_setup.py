from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_driver(browser='chrome', headless=False):
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920x1080')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920x1080')
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    elif browser == 'edge':
        # TODO: Add headless browser
        # No Edge browser to test code
        raise ValueError(f"Unsupported browser: {browser}")
        # driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    driver.implicitly_wait(10)
    return driver
