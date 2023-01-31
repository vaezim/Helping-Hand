from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep


# checking the existence of an element by its CSS Selector
def find_by_css_selector(driver, css_selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException:
        return None
    return element

# wait for <wait> seconds until an element becomes available
# change wait based on the time control of the game
def find_by_css_selector_persist(driver, css_selector, wait=0.2):
    element = find_by_css_selector(driver, css_selector)
    while not element:
        sleep(wait)
        element = find_by_css_selector(driver, css_selector)
    return element
