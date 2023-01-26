# Selenium webdriver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# Chess engine
from stockfish import Stockfish
# Extra functions
from extraUtilities import find_by_css_selector
from math import ceil


# create a Firefox geckodriver
driver = webdriver.Firefox()
driver.get("https://www.chess.com")

# wait for the user to login and start a new game
######## Replace with GUI ########
input("[*] Login and start a new game, then press any key to continue: ")

# detect the color of the player
PLAYER_COLOR = None
white_king = find_by_css_selector("div[class=\"piece wk square-51\"]")
black_king = find_by_css_selector("div[class=\"piece bk square-58\"]")
if white_king.location['y'] > black_king.location['y']:
    PLAYER_COLOR = 'W'
else:
    PLAYER_COLOR = 'B'

# using stockfish engine
ENGINE_PATH = r"..\stockfish_15_win_x64_popcnt\stockfish_15_x64_popcnt"
stockfish = Stockfish(path=ENGINE_PATH, depth=18)
stockfish.update_engine_parameters({"Hash": 2048, "Minimum Thinking Time": 100})
stockfish.set_elo_rating(2500) # playing as a 2500 rated player

# creating a board from the chess library
board = chess.Board()
MOVE_NUM = 0 # counts the total moves played by both players (1. e4 e5 = 2)

# if we are playing black, get the opponent's first move
if PLAYER_COLOR == 'B':
    # find the move's css element
    css_selector = f"div[data-ply=\"{MOVE_NUM}\"]"
    oppMove = find_by_css_selector(css_selector).text
    # push to move to the board and stockfish engine
    UCI = board.push_san(oppMove)
    stockfish.make_moves_from_current_position([UCI.uci()])
    # increment MOVE_NUM
    MOVE_NUM = 1
    ######## Replace with GUI ########
    print(str(ceil(MOVE_NUM/2)) + '. ' + UCI.uci())

# get the best engine move
topMove = stockfish.get_best_move_time(3000)
