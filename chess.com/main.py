# Selenium webdriver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# Extra functions
from extraUtilities import check_exists_by_css_selector
# Chess engine
from stockfish import Stockfish


# Creating a Firefox geckodriver
driver = webdriver.Firefox()
driver.get("https://www.chess.com")

# Wait for the user to login and start a new game
######## Replace with GUI ########
input("[*] Login and start a new game, then press any key to continue: ")

# Detecting the color of the player
PLAYER_COLOR = None
white_king = driver.find_element(By.CSS_SELECTOR, "div[class=\"piece wk square-51\"]")
black_king = driver.find_element(By.CSS_SELECTOR, "div[class=\"piece bk square-58\"]")
if white_king.location['y'] > black_king.location['y']:
    PLAYER_COLOR = 'W'
else:
    PLAYER_COLOR = 'B'

