from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import chess.svg
from time import sleep
import os


# checking the existence of an element by its CSS Selector
def find_by_css_selector(driver, css_selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException:
        return None
    return element

# wait for <wait> seconds until an element becomes available
# change wait based on the time control of the game
def find_by_css_selector_persist(driver, css_selector, wait=0.3):
    element = find_by_css_selector(driver, css_selector)
    while not element:
        sleep(wait)
        element = find_by_css_selector(driver, css_selector)
    return element

def createSVGfromBoard(board, best_move=None):
    OutputFilename = "svg/board.svg"
    if not best_move:
        svg = chess.svg.board(board)
    else:
        sq1, sq2 = best_move[0:2], best_move[2:]
        svg = chess.svg.board(board,\
            arrows=[chess.svg.Arrow(square2num(sq1),\
                                    square2num(sq2), color="blue")])
    with open(OutputFilename, 'w') as file:
        file.write(svg)
    return OutputFilename

def square2num(square):
    col, row = square[0].upper(), square[1]
    return (int(row)-1)*8 + (ord(col)-ord('A'))

def getStockfishEnginePath():
    PATH = r"../dependencies/stockfish/"
    os_name = os.name
    if os_name == "nt": # windows
        PATH += r"stockfish_15_x64_popcnt.exe"
    elif os_name == "posix": # linux
        PATH += r"stockfish-ubuntu-20.04-x86-64"
    return PATH
    
def getGeckodriverPath():
    PATH = r"../dependencies/geckodrivers/"
    os_name = os.name
    if os_name == "nt": # windows
        PATH = r"geckodriver.exe"
    elif os_name == "posix": # linux
        PATH = r"geckodriver"
    return PATH
    
