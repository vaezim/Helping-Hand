from time import sleep


# checking the existence of an element by its CSS Selector
def find_by_css_selector(css_selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException:
        return None
    return element

# wait for <wait> seconds until an element becomes available
def find_by_css_selector_persist(css_selector, wait=2):
    element = find_by_css_selector(css_selector)
    while not element:
        sleep(wait)
        element = find_by_css_selector(css_selector)
    return element
