# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# Chess utilities
from stockfish import Stockfish
import chess
# Extra utilities
from time import sleep
import utils


'''
*** Make sure to activate [Input moves with keyboard] from Preferences/Game Behavior ***
'''

# Setting up Stockfish and chess.board
ENGINE_PATH = utils.getStockfishEnginePath()
stockfish = Stockfish(path=ENGINE_PATH, depth=8)
stockfish.update_engine_parameters({"Hash": 2048, "Minimum Thinking Time": 100})
stockfish.set_elo_rating(2000)
board = chess.Board()

# create a Firefox geckodriver
GECKODRIVER_PATH = utils.getGeckodriverPath()
driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
driver.get("https://www.lichess.org")

# Sign-in button
signin_button = utils.find_by_css_selector(driver, \
                        "a[class=\"signin button button-empty\"]")
signin_button.click()

# Credentials
username = driver.find_element(By.ID, "form3-username")
password = driver.find_element(By.ID, "form3-password")
username.send_keys("AlirezaFriooozja") # edit
password.send_keys("qweasd19982012") # edit
utils.find_by_css_selector(driver, \
        "button[class=\"submit button\"]").click()

# Selecting a time control. playable time controls: 1+0, 3+0, 5+0, 10+0, ...
time_control = utils.find_by_css_selector_persist(driver, \
    "div[data-id=\"3+0\"]")
time_control.click()

# Detecting color
message = utils.find_by_css_selector_persist(driver, \
    "div[class=\"message\"]", wait=1).text.lower()
if "black" in message:
    COLOR = 'B'
else:
    COLOR = 'W'

# Creating a handle for the move input box
move_handle = driver.find_element(By.CLASS_NAME, "ready")
move_handle.send_keys(Keys.RETURN)

# LAST move's element: <kwdb class="alt">move_text</kwdv>
if COLOR == 'B':
    oppMove = utils.find_by_css_selector_persist(driver, \
        "kwdb[class=\"alt\"]").text
    UCI = board.push_san(oppMove)
    stockfish.make_moves_from_current_position([UCI.uci()])

# Play until checkmate...
while not board.is_checkmate():

    # User's move
    myMove = stockfish.get_best_move_time()
    move_handle.clear()
    move_handle.send_keys(myMove)
    stockfish.make_moves_from_current_position([myMove])
    board.push_uci(myMove)

    # Opponent's move
    oppMove = utils.find_by_css_selector_persist(driver, \
        "kwdb[class=\"alt\"]").text
    while oppMove == myMove:
        sleep(0.5)
        oppMove = utils.find_by_css_selector_persist(driver, \
        "kwdb[class=\"alt\"]").text
    UCI = board.push_san(oppMove)
    stockfish.make_moves_from_current_position([UCI.uci()])
