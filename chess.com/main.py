# Selenium
from selenium import webdriver
# GUI
from PyQt5.QtWidgets import QApplication
from AppWindow import MainWindow
# Chess utilities
from stockfish import Stockfish
import chess
# Extra functions
from math import ceil
import utils
import sys
from threading import Thread
import json

with open('config.json') as config_file:
    data = json.load(config_file)

# creates a Firefox geckodriver
GECKODRIVER_PATH = utils.getGeckodriverPath()
driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
driver.get("https://www.chess.com")

# creates App window
app = QApplication(sys.argv)
global window
window = MainWindow()
window.show()

# using stockfish engine
ENGINE_PATH = utils.getStockfishEnginePath()
stockfish = Stockfish(path=ENGINE_PATH, depth=data["engine"]["depth"])
stockfish.update_engine_parameters({"Hash": data["engine"]["hash"], "Threads": data["engine"]["threads"]})
if data["engine"]["skill_level"] < 0:
    stockfish.set_elo_rating(data["engine"]["elo"])
else:
    stockfish.set_skill_level(data["engine"]["skill_level"])
# creating a board from the chess library
board = chess.Board()
# making them accessible from the window
window.setChessComponents(board, stockfish) 

def SeleniumFunction():
    id = window.grandId
    print("New board started...")
    MOVE_NUM = 1

    board = chess.Board()

    # detects the color of the player
    PLAYER_COLOR = None
    white_king = utils.find_by_css_selector_persist(driver, "div[class=\"piece wk square-51\"]", wait=2)
    black_king = utils.find_by_css_selector_persist(driver, "div[class=\"piece bk square-58\"]", wait=2)
    if white_king.location['y'] > black_king.location['y']:
        PLAYER_COLOR = 'W'
    else:
        PLAYER_COLOR = 'B'

    while True:
        # next move's css
        css_selector = f"div[data-ply=\"{MOVE_NUM}\"]"
        
        # checks for your turn or not
        if (board.turn == chess.WHITE and PLAYER_COLOR == 'W') or (board.turn == chess.BLACK and PLAYER_COLOR == 'B'):
            window.doEvaluation()

        if id != window.grandId:
            break

        # waits for the player to make his move
        move = utils.find_by_css_selector_persist(driver, css_selector, wait=0.1).text

        if id != window.grandId:
            break

        # adds the move to the board and stockfish engine
        try:
            UCI = board.push_san(move)
        except:
            print("Illegal San, try again!")
            continue

        if id != window.grandId:
            break

        stockfish.make_moves_from_current_position([UCI.uci()])
        evaluation = stockfish.get_evaluation()

        # generates board SVG and updates gui window
        OutputFilename = utils.createSVGfromBoard(board)
        window.evalThread.updateEval(evaluation)
        window.boardSvgThread.updateBoard(OutputFilename)

        if id != window.grandId:
            break
        
        MOVE_NUM += 1

    startFunction()

#def gameOver():
#    endBoard = utils.find_by_css_selector(driver, "div[class=\"board-modal-container-container\"]")
#    if endBoard:
#        return True
#    return False

def startFunction():
    selenium_thread = Thread(target=SeleniumFunction)
    selenium_thread.start()

startFunction()

sys.exit(app.exec_())
