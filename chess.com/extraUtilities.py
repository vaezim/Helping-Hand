
# Checking the existence of an element by its CSS Selector
def check_exists_by_css_selector(css_selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException:
        return False
    return element

