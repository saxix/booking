import pytest
from selenium import webdriver
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver, WebDriver
    from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver

browsers = {
    "firefox": webdriver.Firefox,
    "chrome": webdriver.Chrome,
}


@pytest.fixture(scope="session")
def chrome_options(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-translate")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--lang=en-GB")
    options.add_argument("--no-sandbox")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--start-maximized")

    prefs = {"profile.default_content_setting_values.notifications": 1}  # explicitly allow notifications
    options.add_experimental_option("prefs", prefs)

    return options


@pytest.fixture(scope="session")
def ff_options(request):
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    return options


@pytest.fixture(scope="session", params=list(browsers.keys()))
def driver(request, chrome_options, ff_options) -> "WebDriver":
    if request.param == "chrome":
        b = browsers[request.param](options=chrome_options)
    else:
        b = browsers[request.param](options=ff_options)

    request.addfinalizer(lambda *args: b.quit())
    return b


@pytest.fixture(scope="session")
def browser(live_server, driver: "ChromeWebDriver | FirefoxWebDriver"):
    driver.live_server = live_server
    driver.set_window_size(1024, 768)
    driver.implicitly_wait(10)
    return driver


@pytest.fixture(autouse=True)
def data(booking, car):
    pass
