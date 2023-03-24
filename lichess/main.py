# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# Chess utilities
from stockfish import Stockfish
import chess
# Extra utilities
from random import random
from time import sleep
import utils
import sys
import json

with open('config.json') as config_file:
data = json.load(config_file)

'''
*** Make sure to activate [Input moves with keyboard] from Preferences/Game-Behavior ***
'''

# Credentials
USERNAME = data["account"]["username"]
PASSWORD = data["account"]["password"]
if not len(USERNAME):
    print("Enter your credentials in the source file!")
    sys.exit()

# Setting up Stockfish and chess.board
ENGINE_PATH = utils.getStockfishEnginePath()
stockfish = Stockfish(path=ENGINE_PATH, depth=data["engine"]["depth"])
stockfish.update_engine_parameters({"Hash": data["engine"]["hash"], "Minimum Thinking Time": 20})
stockfish.set_elo_rating(data["engine"]["elo"])
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
username.send_keys(USERNAME)
password.send_keys(PASSWORD)
utils.find_by_css_selector(driver, \
        "button[class=\"submit button\"]").click()

# Select a time control
print("Select a time control.")

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

# element containing moves: <l4x>
if COLOR == 'B':
    moves_text = utils.find_by_css_selector_persist(driver, "l4x").text
    oppMove = utils.extractLastMove(moves_text)
    UCI = board.push_san(oppMove)
    stockfish.make_moves_from_current_position([UCI.uci()])

# Play until checkmate...
while not board.is_checkmate():

    # User's move (uci)
    myMove = stockfish.get_best_move_time(data["engine"]["max_time"])
    move_handle.clear()
    sleep(0.25)
    move_handle.send_keys(myMove[0:2])
    sleep(0.25)
    move_handle.send_keys(myMove[2:])
    stockfish.make_moves_from_current_position([myMove])
    board.push_uci(myMove)

    # Opponent's move (san)
    while True:
        sleep(random()*5) # wait for [0-5] seconds
        moves_text = utils.find_by_css_selector_persist(driver, "l4x").text
        oppMove = utils.extractLastMove(moves_text)
        if oppMove == 0:
            print("Game Ended.")
            sys.exit()
        try:
            UCI = board.push_san(oppMove)
            stockfish.make_moves_from_current_position([UCI.uci()])
            break;
        except:
            continue
