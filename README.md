# 🤖 Online Chess Cheater Bot
[lichess.org](https://lichess.org/) and [chess.com](https://chess.com) are the two most popular online chess platforms. This application provides the user with the top engine move and position evaluation. Once a live online game is started, it automatically pulls the played moves from the webpage's source and builds it own chess board. A local stockfish engine then analyzes the position and offers the best move to the user.

## ⚠️ Disclaimer!
This application was for learning purposes only! Excessive usage of this bot can get your acount banned! see [lichess Terms of Service](https://lichess.org/terms-of-service) and [chess.com Terms of Service](https://www.chess.com/legal/user-agreement)

## 💿 Dependencies
- [Selenium](https://www.selenium.dev/): offers remote control of webdrivers for website testing and automation. This [link](https://selenium-python.readthedocs.io/) provides a great documentation on how to use selenium in Python.
- You need to download a [webdriver](https://selenium-python.readthedocs.io/installation.html#drivers) for your browser to be able to use selenium.
- [Stockfish](https://stockfishchess.org/): currently the best chess engine available. You need to download the engine's command-line program.
- [Python API for Stockfish](https://pypi.org/project/stockfish/): Stockfish's python API.

## 💻 Usage
### ♟️ Chess.com
1. `cd chess.com`
2. `python3 main.py` and wait for both windows to open.
3. login to your chess.com account and start a game.
4. The board and the evaluation bar are constantly updated, and you have to wait a bit to get the best move arrow after opponent's move.

![](chess.com/Animation.gif)

### ♘ Lichess
*This is an automated app. It logs in to your lichess accout, picks bullet time control, and beats the opponent.*
1. Activate **[Input moves with keyboard]** from Preferences/Game Behavior.
2. Enter your Lichess credentials in the dedicated place in the source file. 
3. Once you run the program it will create a webdriver instance, request lichess website and sign in using your credentials. 
4. Select a time control.
5. From now on the moves are made by the bot until the match is over.

![](lichess/Animation.gif)
