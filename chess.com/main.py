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

# making the board and stockfish accessible from the window
window.setChessComponents(chess.Board(), stockfish) 

def SeleniumFunction():
    id = window.grandId
    print(f"New board of id {id} started...")
    MOVE_NUM = 1

    stockfish.set_position(None) # resets stockfish internal board

    window.board = chess.Board() # resets chess library board

    # detects the color of the player
    PLAYER_COLOR = None
    white_king = utils.find_by_css_selector_persist(driver, "div[class=\"piece wk square-51\"]", id, window, wait=0.5)
    black_king = utils.find_by_css_selector_persist(driver, "div[class=\"piece bk square-58\"]", id, window, wait=0.5)
    if id != window.grandId:
        return startFunction()

    if white_king.location['y'] > black_king.location['y']:
        PLAYER_COLOR = 'W'
    else:
        PLAYER_COLOR = 'B'

    print("Board found!")

    while True:
        # next move's css
        css_selector = f"div[data-ply=\"{MOVE_NUM}\"]"
        
        # checks for your turn or not
        if (window.board.turn == chess.WHITE and PLAYER_COLOR == 'W') or (window.board.turn == chess.BLACK and PLAYER_COLOR == 'B'):
            window.doEvaluation()

        if id != window.grandId:
            break

        # waits for the player to make his move
        move = utils.find_by_css_selector_persist(driver, css_selector, id, window, wait=0.1)

        if id != window.grandId:
            break

        # adds the move to the board and stockfish engine
        try:
            UCI = window.board.push_san(move.text)
        except:
            print("Illegal San, try again!")
            continue

        if id != window.grandId:
            break

        stockfish.make_moves_from_current_position([UCI.uci()])
        evaluation = stockfish.get_evaluation()

        # generates board SVG and updates gui window
        OutputFilename = utils.createSVGfromBoard(window.board)
        window.evalThread.updateEval(evaluation)
        window.boardSvgThread.updateBoard(OutputFilename)

        if id != window.grandId:
            break
        
        MOVE_NUM += 1

    return startFunction()

# Like I'm not sure of what i've done, so a button is better work lol
#def gameOver():
#    endBoard = utils.find_by_css_selector(driver, "div[class=\"board-modal-container-container\"]")
#    if endBoard:
#        return True
#    return False

def startFunction():
    window.grandId+=1
    selenium_thread = Thread(target=SeleniumFunction)
    selenium_thread.start()

startFunction()

sys.exit(app.exec_())
