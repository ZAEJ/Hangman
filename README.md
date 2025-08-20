
# Hangman GUI Game

## Overview
This is a graphical Hangman game built with Python and Tkinter. Guess the hidden word or phrase by selecting letters or entering your guess. The game supports categories, difficulty levels, hints, and keeps track of your high score.

## How to Play
1. **Start the Game:**
	- Run the game with:
	  ```
	  python hangman_gui.py
	  ```
	- The main window will open with the Hangman image, category, and input fields.

2. **Game Controls:**
	- **Guess a Letter:** Type a letter in the input box or click a letter button.
	- **Guess the Phrase:** Type the full word or phrase and press Enter or click Submit.
	- **Settings:** Click the "Configuración" (Settings) button (top right) to change difficulty, category, mode (single/multiplayer), enable/disable hints, or switch language.
	- **Restart:** Click "Reiniciar Juego" (Restart Game) to start a new round.

3. **Game Rules:**
	- You have a limited number of incorrect guesses (based on difficulty).
	- Each wrong guess draws another part of the hangman.
	- Use hints if enabled (after several wrong guesses).
	- Win by guessing all letters or the full phrase before running out of attempts.
	- Your score increases with each win. High scores are saved.

4. **Multiplayer Mode:**
	- Choose "Multijugador" in settings. One player enters a word/phrase and (optionally) a category for the other to guess.

## Requirements
- Python 3.x
- Tkinter (usually included with Python)
- Pillow (for image support):
  ```
  pip install pillow
  ```

## Assets
- Images are in the `images/` folder.
- Word lists are in `src/words.txt`.
- Sounds are in `src/sounds/`.

## Troubleshooting
- If images or sounds do not load, check that the asset folders are present and paths are correct.
- For any errors, run the script from the project root directory.

## Enjoy the game!