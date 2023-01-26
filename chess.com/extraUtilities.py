
# Checking the existence of an element by its CSS Selector
def find_by_css_selector(css_selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException:
        return None
    return element

