#!/usr/bin/python3

# Selenium
from selenium import webdriver
# GUI
from PyQt5.QtWidgets import QApplication
from AppWindow import MainWindow
# Chess utilities
from stockfish import Stockfish
import chess
# Extra functions
import utils
import sys
from threading import Thread
import json

with open('config.json') as config_file:
    config = json.load(config_file)

# create a Firefox geckodriver
GECKODRIVER_PATH = utils.getGeckodriverPath()
driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
driver.get("https://www.chess.com")

# create App window
app = QApplication(sys.argv)
global window
window = MainWindow()
window.show()

# using stockfish engine
ENGINE_PATH = utils.getStockfishEnginePath()
stockfish = Stockfish(path=ENGINE_PATH, depth=config["engine"]["depth"])
stockfish.update_engine_parameters({"Hash": config["engine"]["hash"], "Minimum Thinking Time": config["engine"]["min_time"]})
stockfish.set_elo_rating(config["engine"]["elo"])
# creating a board from the chess library
board = chess.Board()
# making them accessible from the window
window.setChessComponents(board, stockfish)

def SeleniumFunction():
    print("Chess.com Bot Started...")
    MOVE_NUM = 1

    # detect the color of the player
    PLAYER_COLOR = None
    white_king = utils.find_by_css_selector_persist(driver, "div[class=\"piece wk square-51\"]", wait=5)
    black_king = utils.find_by_css_selector_persist(driver, "div[class=\"piece bk square-58\"]", wait=5)
    if white_king.location['y'] > black_king.location['y']:
        PLAYER_COLOR = 'W'
    else:
        PLAYER_COLOR = 'B'

    while True:
        # next move's css
        css_selector = f"div[config-ply=\"{MOVE_NUM}\"]"

        # wait for the player to make his move
        move = utils.find_by_css_selector_persist(driver, css_selector, wait=0.3).text

        # add the move to the board and stockfish engine
        try:
            UCI = board.push_san(move)
        except:
            print("Illegal San, try again!")
            continue

        stockfish.make_moves_from_current_position([UCI.uci()])
        evaluation = stockfish.get_evaluation()

        # generate board SVG and update gui window
        OutputFilename = utils.createSVGfromBoard(board)
        window.evalThread.updateEval(evaluation)
        window.boardSvgThread.updateBoard(OutputFilename)
        
        MOVE_NUM += 1

selenium_thread = Thread(target=SeleniumFunction)
selenium_thread.start()
sys.exit(app.exec_())
