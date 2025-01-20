import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from booking.utils.fixtures import UserFactory

GH_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def wait_for(driver, *args):
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, 10)
    wait.until(ec.visibility_of_element_located((*args,)))
    return driver.find_element(*args)


def find_by_css(driver, *args):
    return wait_for(driver, By.CSS_SELECTOR, *args)


@pytest.mark.skipif(GH_ACTIONS, reason="Selenium test non abilitati in GitHub Actions.")
def test_login(browser, user):
    browser.get(f"{browser.live_server}/")
    wait_for(browser, By.LINK_TEXT, "Login").click()
    wait = WebDriverWait(browser, 10)
    wait.until(ec.url_contains("/login/"))

    find_by_css(browser, "input[name=username").send_keys(user.username)
    find_by_css(browser, "input[name=password").send_keys(UserFactory._password)
    wait_for(browser, By.TAG_NAME, "button").click()

    wait_for(browser, By.LINK_TEXT, "Your bookings")
    wait_for(browser, By.LINK_TEXT, "Fleet").click()
