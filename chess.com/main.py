# Selenium webdriver
from selenium import webdriver
# Chess engine
from stockfish import Stockfish
import chess
# Extra functions
from utils import find_by_css_selector, find_by_css_selector_persist
from math import ceil


# create a Firefox geckodriver
driver = webdriver.Firefox()
driver.get("https://www.chess.com")

# using stockfish engine
ENGINE_PATH = r"../stockfish-ubuntu-20.04-x86-64"
stockfish = Stockfish(path=ENGINE_PATH, depth=10)
stockfish.update_engine_parameters({"Hash": 2048, "Minimum Thinking Time": 100})
stockfish.set_elo_rating(2000)

# creating a board from the chess library
board = chess.Board()

# wait for the user to login and start a new game
######## Replace with GUI ########
input("[*] Login and start a new game, then press any key to continue: ")

# detect the color of the player
PLAYER_COLOR = None
white_king = find_by_css_selector(driver, "div[class=\"piece wk square-51\"]")
black_king = find_by_css_selector(driver, "div[class=\"piece bk square-58\"]")
if white_king.location['y'] > black_king.location['y']:
    PLAYER_COLOR = 'W'
else:
    PLAYER_COLOR = 'B'

ENOUGH = False
while not ENOUGH:
    # counts the total moves played by both players (e4=1 & e5=2)
    MOVE_NUM = 1

    while True:
        # next move's css
        css_selector = f"div[data-ply=\"{MOVE_NUM}\"]"

        # wait for the player to make his move
        move = find_by_css_selector_persist(driver, css_selector).text

        # add the move to the board and stockfish engine
        UCI = board.push_san(move)
        stockfish.make_moves_from_current_position([UCI.uci()])
        # get the best engine move
        print(stockfish.get_evaluation()["value"]/100)
        topMove = stockfish.get_best_move_time(3000)
        MOVE_NUM += 1

        ######## Replace with GUI ########
        print(f"{ceil(MOVE_NUM/2)}. {move} (top move = {topMove})")
        