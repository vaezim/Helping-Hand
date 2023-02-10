from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stockfish import Stockfish
from time import sleep
from math import ceil
import random
import chess
import time
'''
*** Make sure to activate [Input moves with keyboard] from Preferences/Game Behavior ***
'''

random.seed(8234798734)

    # Checking the existence of an element by its XPATH
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return driver.find_element(By.XPATH, xpath)

    # Creating a Firefox geckodriver and requesting lichess.org
driver = webdriver.Firefox()
driver.get("https://www.lichess.org")

    # Signing in
signin_button = driver.find_element(by=By.XPATH, value="/html/body/header/div[2]/a")
signin_button.click()
username = driver.find_element(By.ID, "form3-username")
password = driver.find_element(By.ID, "form3-password")
username.send_keys("Username") # your credentials here
password.send_keys("Password")
driver.find_element(By.XPATH, "/html/body/div/main/form/div[1]/button").click() # submit

print('Press [ENTER] to Start:')
input('>> ')

bullet_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]")
bullet_button.click()

WAIT = 3
for i in range(WAIT):
    print("Starting in " + str(WAIT-i))
    sleep(1)

game_over = False
timeout = False

while not game_over:
    if timeout:
        MOVE_NUM = 0
        timeout = False

    input('Ready? >> ')    

        # If a message box, indicating that it's our move, exists then we're white,
        # O.W. an "Unable to locate element" error is raised.
    try:
        message = driver.find_element(By.XPATH,
            "/html/body/div[1]/main/div[1]/rm6/div[2]")
        COLOR = 'W'
    except:
        COLOR = 'B'
 
        # Creating a handle for the move input box
    move_handle = driver.find_element(By.CLASS_NAME, "ready")
    move_handle.send_keys(Keys.RETURN)

        # Using Stockfish Engine & chess.board
    ENGINE_PATH = r"..\stockfish_15_win_x64_popcnt\stockfish_15_x64_popcnt"
    stockfish = Stockfish(path=ENGINE_PATH, depth=18)
    stockfish.update_engine_parameters({"Hash": 2048, "Minimum Thinking Time": 100})
    stockfish.set_elo_rating(2500) # playing as a 2500 rated

    board = chess.Board()
    MOVE_NUM = 1

    if COLOR == 'B':
        oppMove = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/rm6/l4x/u8t[" + str(MOVE_NUM) + "]").text
        UCI = board.push_san(oppMove)
        stockfish.make_moves_from_current_position([UCI.uci()])
        print(str(ceil(MOVE_NUM/2)) + '. ' + UCI.uci())
    else:
        MOVE_NUM = 0

    myMove = stockfish.get_best_move_time(3000)
    stockfish.make_moves_from_current_position([myMove])
    print(str(ceil((MOVE_NUM + 1) / 2)) + '. ' + myMove)
    board.push_uci(myMove)
    move_handle.clear()
    move_handle.send_keys(myMove)
    MOVE_NUM += 2

    while not board.is_checkmate():
        try:
            oppXpath = "/html/body/div[1]/main/div/rm6/l4x/u8t[" + str(MOVE_NUM) + "]"
            wait = WebDriverWait(driver, 30) # if this time is too long to wait lower it but 30 seconds I found prevents accidental restarts due to slow opponents
            oppMove = wait.until(EC.presence_of_element_located((By.XPATH, oppXpath))).text
        except TimeoutException:
            timeout = True
            break

        oppMove = check_exists_by_xpath(oppXpath).text
        UCI = board.push_san(oppMove)
        stockfish.make_moves_from_current_position([UCI.uci()])
        print(str(ceil(MOVE_NUM / 2)) + '. ' + UCI.uci())
        myMove = stockfish.get_best_move_time(round(random.random() * 2000))  # random time from [0,2]s
        stockfish.make_moves_from_current_position([myMove])
        print(str(ceil((MOVE_NUM + 1) / 2)) + '. ' + myMove)
        board.push_uci(myMove)
        move_handle.clear()
        move_handle.send_keys(myMove)
        MOVE_NUM += 2
