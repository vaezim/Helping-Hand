# 🤖 Online Chess Bot
[lichess.org](https://lichess.org/) and [chess.com](https://chess.com) are the two most popular online chess platforms. This application provides the user with the top engine move and position evaluation. Once a live online game is started, it automatically pulls the played moves from the webpage's source and helps you do a move. A local stockfish engine then analyzes the position and offers the best move to the user.

## ⚠️ Disclaimer!
This application was for learning purposes only! Excessive usage of this bot can get your acount banned! see [lichess Terms of Service](https://lichess.org/terms-of-service) and [chess.com Terms of Service](https://www.chess.com/legal/user-agreement)

## 💿 Dependencies
- [Selenium](https://www.selenium.dev/): offers remote control of webdrivers for website testing and automation. This [link](https://selenium-python.readthedocs.io/) provides a great documentation on how to use selenium in Python.
- You need to download a [webdriver](https://selenium-python.readthedocs.io/installation.html#drivers) for your browser to be able to use selenium.
- [Stockfish](https://stockfishchess.org/): currently the best chess engine available. You need to download the engine's command-line program.
- [Python API for Stockfish](https://pypi.org/project/stockfish/): Stockfish's python API.
- [Firefox](https://www.mozilla.org/en-US/firefox/new/): used for the project

## 💻 Usage
### ♟️ Chess.com
1. Open `chess.com.bat` and wait for both windows to open.
2. Log into your chess.com account and start a game.
3. The board and the evaluation bar are constantly updated, and you have to wait a bit to get the best move arrow after opponent's move.

![](chess.com/Animation.gif)

### ♘ Lichess
*This is an automated app. It logs in to your lichess accout, picks bullet time control, and beats the opponent. More customisation will be added later.*
1. Activate **[Input moves with keyboard]** from Preferences/Game Behavior.
2. Enter your Lichess credentials in the dedicated place in the config file *lichess/config.json*. 
3. Once you open `lichess.bat` it will create a webdriver instance, request lichess website and sign in using your credentials. 
4. Select a time control.
5. From now on the moves are made by the bot until the match is over.

![](lichess/Animation.gif)

## How to config?
Open the configuration file *avaible in the folders chess.com and lichess*. In it, you have different options.
- **window/-**: The size of the window *chess.com only*
- **account/-**: Put your account username and password in so the program can log in by itself *lichess only*
- **engine/elo**: The level of the engine
- **engine/depth**: How depth will the engine watch in the possible moves. Higher values = Slower to calculate, but won't above the max_time value.
- **engine/hash**: To not lose what is already calculated and win a bit of time. It is in MB (uses Ram), and must be a power of 2 (2,4,8,16,...)
- **engine/max_time**: The maximum time in milliseconds the engine has to calculate the move