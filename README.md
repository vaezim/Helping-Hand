# 🤖 Lichess Cheater Bot
[Lichess](https://lichess.org/) is an open-source online chess platform. This program signs in to your lichess account, picks a time control, and beats the opponent with the best engine moves.

## ⚠️ Disclaimer!
Too much usage of this bot can get your acount banned! [Lichess Terms of Service](https://lichess.org/terms-of-service)

## 💿 Dependencies
- [Selenium](https://www.selenium.dev/): Offers remote control of webdrivers for website testing and automation. This [link](https://selenium-python.readthedocs.io/) provides a great documentation on how to use selenium in Python.
- You need to download a [webdriver](https://selenium-python.readthedocs.io/installation.html#drivers) for the browser of your own choice to be able to use selenium.
- [Stockfish](https://stockfishchess.org/): current best chess engine available. You need to download the engine's command-line program.
- [Python API for Stockfish](https://pypi.org/project/stockfish/): Stockfish's python API.

## 💻 Usage
1. *Make sure to activate [Input moves with keyboard] from Preferences/Game Behavior*
2. Enter your Lichess credentials in the dedicated place. 
3. Once you run the program it will create a webdriver instance, request lichess website and sign in using your credentials. 
4. Wait for the page to be fully loaded. A prompt will appear. By pressing a key a bullet game will be started. 
5. A second prompt lets you start the game. From now on the moves are made by the bot until the match is over.

![](Animation.gif)
