import random
import winsound
import os
import unicodedata
import time
import sys
import threading

def print_lose_art():
    print(r"""
 __     __           _                    _ 
 \ \   / /          | |                  | |
  \ \_/ /__  _   _  | |     ___  ___  ___| |
   \   / _ \| | | | | |    / _ \/ __|/ _ \ |
    | | (_) | |_| | | |___| (_) \__ \  __/_|
    |_|\___/ \__,_| |______\___/|___/\___(_)
    """)

import random
import winsound
import os
import unicodedata
import time
import sys
import threading


# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def color_text(text, color):
    return f"{color}{text}{Colors.RESET}"

def main():
    print(color_text("Welcome to my Python project!", Colors.CYAN))
    score = 0
    high_score = load_high_score()
    while True:
        print(color_text("\nGame Modes:", Colors.YELLOW))
        print("1. Single Player (random word)")
        print("2. Multiplayer (player enters word/phrase)")
        mode = input("Choose mode (1 or 2): ").strip()
        if mode == '2':
            word = input("Player 1, enter a word or phrase for Player 2 to guess: ").strip()
            category = input("Enter a category for this word/phrase (optional): ").strip()
            won = play_hangman(color_text, Colors, word, category, multiplayer=True)
        else:
            categories = load_categories()
            print(color_text("\nAvailable categories:", Colors.YELLOW))
            for idx, cat in enumerate(categories.keys(), 1):
                print(f"{idx}. {cat}")
            cat_choice = input("Choose a category by number or press Enter for random: ").strip()
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
                cat_name = list(categories.keys())[int(cat_choice)-1]
                word = random.choice(categories[cat_name])
                category = cat_name
            else:
                cat_name = random.choice(list(categories.keys()))
                word = random.choice(categories[cat_name])
                category = cat_name
            won = play_hangman(color_text, Colors, word, category)
        if won:
            score += 1
            if score > high_score:
                high_score = score
                save_high_score(high_score)
                print(color_text(f"New High Score: {high_score}!", Colors.CYAN))
        print(f"Current score: {score} | High score: {high_score}")
        again = input("Do you want to play again? (y/n): ").strip().lower()
        if again != 'y':
            print_game_over_art()
            print(f"Final score: {score}")
            break

def play_hangman(color_text, Colors, word, category=None, multiplayer=False):
    # Setup sounds
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sounds_dir = os.path.join(base_dir, 'src', 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    win_path = os.path.join(sounds_dir, 'win2.wav')
    game_over_path = os.path.join(sounds_dir, 'game_over.wav')
    lose_path = os.path.join(sounds_dir, 'lose.wav')
    if not os.path.exists(win_path):
        generate_win_sound(win_path)
    if not os.path.exists(game_over_path):
        generate_game_over_sound(game_over_path)
    if not os.path.exists(lose_path):
        generate_lose_sound(lose_path)

    # Choose difficulty
    print("\nSelect difficulty level:")
    print("1. Easy (10 attempts)")
    print("2. Normal (6 attempts)")
    print("3. Hard (4 attempts)")
    while True:
        diff = input("Enter 1, 2, or 3: ").strip()
        if diff == '1':
            attempts = 10
            break
        elif diff == '2':
            attempts = 6
            break
        elif diff == '3':
            attempts = 4
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    word_lower = word.lower()
    guessed = set()
    guessed_display = set()
    all_letters = set('abcdefghijklmnopqrstuvwxyz0123456789')
    print(color_text("\nLet's play Hangman!", Colors.YELLOW))
    if category:
        print(color_text(f"Category: {category}", Colors.CYAN))
    if multiplayer:
        print(color_text("(Multiplayer mode)", Colors.YELLOW))

    def display_word():
        return ' '.join([
            letter if (remove_accents(letter.lower()) in guessed or not letter.isalnum()) else '_'
            for letter in word
        ])

    wrong_guesses = 0
    hint_used = False
    import time
    import string
    while attempts > 0:
        print(f"\nWord: {display_word()}")
        print(f"Attempts left: {color_text(str(attempts), Colors.CYAN)}")
        print(f"Guessed: {color_text(' '.join(sorted(guessed_display)) if guessed_display else '-', Colors.YELLOW)}")
        guessed_display_noacc = set(remove_accents(g.lower()) for g in guessed_display)
        unused = all_letters - guessed_display_noacc
        print(f"Unused letters: {color_text(' '.join(sorted(unused)), Colors.YELLOW)}")
        # Timed mode: 15 seconds per guess
        guess = timed_input("Guess a letter, number, or the whole phrase: ", 15)
        if guess is None:
            print(color_text("Time's up! You lost an attempt.", Colors.RED))
            attempts -= 1
            continue
        guess = guess.strip().lower()

        if not guess:
            print("Please enter a guess.")
            continue

        # Only allow alphabetic or numeric input for single characters
        if len(guess) == 1 and not guess.isalnum():
            print("Please enter a valid letter or number.")
            continue

        # Accent-insensitive guess
        guess_no_acc = remove_accents(guess)
        word_no_acc = remove_accents(word_lower)

        # Guessing the whole phrase
        if len(guess) > 1:
            if guess_no_acc == word_no_acc:
                guessed.update([remove_accents(c.lower()) for c in word if c.isalnum()])
                print(color_text(f"Congratulations! You guessed the phrase: {word}", Colors.GREEN))
                time.sleep(0.5)
                play_sound(win_path)
                time.sleep(0.5)
                # play_sound(game_over_path)
                return True
            else:
                attempts -= 1
                print(color_text("Wrong phrase guess.", Colors.RED))
                continue

        # Guessing a single character
        if len(guess) != 1:
            print("Please enter a single character or the whole phrase.")
            continue

        if guess_no_acc in guessed or guess in guessed_display:
            print("You already guessed that character.")
            continue

        guessed_display.add(guess)

        word_noacc_set = set(remove_accents(c.lower()) for c in word if c != ' ')
        if guess_no_acc in word_noacc_set:
            guessed.add(guess_no_acc)
            print(color_text("Good guess!", Colors.GREEN))
        else:
            attempts -= 1
            wrong_guesses += 1
            print(color_text("Wrong guess.", Colors.RED))
            print_hangman(attempts)
            # Offer a hint after 3 wrong guesses, only once
            if wrong_guesses == 3 and not hint_used:
                use_hint = input("Would you like a hint? (y/n): ").strip().lower()
                if use_hint == 'y':
                    # Reveal a random unguessed letter
                    unguessed = [remove_accents(c.lower()) for c in word if c.isalnum() and remove_accents(c.lower()) not in guessed]
                    if unguessed:
                        hint_letter = random.choice(unguessed)
                        guessed.add(hint_letter)
                        print(color_text(f"Hint: The word contains the letter '{hint_letter}'.", Colors.CYAN))
                        hint_used = True
                    else:
                        print(color_text("No more letters to reveal!", Colors.YELLOW))
                        hint_used = True
        if all((remove_accents(c.lower()) in guessed or not c.isalnum()) for c in word):
            print_win_art()
            print(color_text(f"\nCongratulations! You guessed the phrase: {word}", Colors.GREEN))
            time.sleep(0.5)
            play_sound(win_path)
            time.sleep(0.5)
            # play_sound(game_over_path)
            return True

    # If loop exits, player lost
    print_hangman(attempts)
    print_lose_art()
    print_game_over_art()
    print(color_text(f"Game over! The phrase was: {word}", Colors.RED))
    play_sound(lose_path)
    play_sound(game_over_path)
    return False
# --- Category and High Score helpers ---
def load_categories():
    # Example: categories from src/words.txt as "Category: word1, word2, ..."
    base_dir = os.path.dirname(os.path.abspath(__file__))
    words_path = os.path.join(base_dir, "src", "words.txt")
    categories = {}
    try:
        with open(words_path, "r", encoding="utf-8") as f:
            current_cat = "General"
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.endswith(":"):
                    current_cat = line[:-1]
                    categories[current_cat] = []
                else:
                    categories.setdefault(current_cat, []).append(line)
        if not categories:
            categories = {"General": ["python", "hangman", "challenge", "programming", "bootcamp"]}
    except Exception:
        categories = {"General": ["python", "hangman", "challenge", "programming", "bootcamp"]}
    return categories

def load_high_score():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        hs_path = os.path.join(base_dir, "highscore.txt")
        if os.path.exists(hs_path):
            with open(hs_path, "r") as f:
                return int(f.read().strip())
    except Exception:
        pass
    return 0

def save_high_score(score):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        hs_path = os.path.join(base_dir, "highscore.txt")
        with open(hs_path, "w") as f:
            f.write(str(score))
    except Exception:
        pass

# --- Timed input helper ---
def timed_input(prompt, timeout):
    result = [None]
    def inner():
        try:
            result[0] = input(prompt)
        except Exception:
            result[0] = None
    t = threading.Thread(target=inner)
    t.daemon = True
    t.start()
    t.join(timeout)
    if t.is_alive():
        return None
    return result[0]
def print_win_art():
    print(r"""
 __     __          __          ___       _ 
 \ \   / /          \ \        / (_)     | |
  \ \_/ /__  _   _   \ \  /\  / / _ _ __ | |
   \   / _ \| | | |   \ \/  \/ / | | '_ \| |
    | | (_) | |_| |    \  /\  /  | | | | |_|
    |_|\___/ \__,_|     \/  \/   |_|_| |_(_)
    """)

def print_game_over_art():
        print(r"""
     _____                         ____                 
    / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
    \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
        """)

def play_sound(sound_path):
    """Play a sound with error handling"""
    try:
        if os.path.exists(sound_path):
            winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        else:
            print(f"Sound file not found: {sound_path}")
    except Exception as e:
        print(f"Error playing sound: {e}")

def generate_win_sound(file_path):
    """Generate a simple win sound"""
    try:
        import numpy as np
        from scipy.io import wavfile
        
        # Generate a cheerful sound
        sample_rate = 44100
        t = np.linspace(0, 1.5, int(sample_rate * 1.5))
        sound = np.sin(2 * np.pi * 523.25 * t) * np.exp(-t)  # C5 note
        sound += np.sin(2 * np.pi * 659.25 * t) * np.exp(-t)  # E5 note
        sound += np.sin(2 * np.pi * 783.99 * t) * np.exp(-t)  # G5 note
        
        # Normalize to 16-bit range
        sound = np.int16(sound / np.max(np.abs(sound)) * 32767)
        
        # Write to file
        wavfile.write(file_path, sample_rate, sound)
        print(f"Generated win sound at {file_path}")
    except ImportError:
        print("Could not generate win sound - required libraries not available")

def generate_game_over_sound(file_path):
    """Generate a simple game over sound"""
    try:
        import numpy as np
        from scipy.io import wavfile
        
        # Generate a dramatic sound
        sample_rate = 44100
        t = np.linspace(0, 2.0, int(sample_rate * 2.0))
        sound = np.sin(2 * np.pi * 196.00 * t) * np.exp(-t*2)  # G3 note
        sound += 0.5 * np.sin(2 * np.pi * 146.83 * t) * np.exp(-t*2)  # D3 note
        
        # Normalize to 16-bit range
        sound = np.int16(sound / np.max(np.abs(sound)) * 32767)
        
        # Write to file
        wavfile.write(file_path, sample_rate, sound)
        print(f"Generated game over sound at {file_path}")
    except ImportError:
        print("Could not generate game over sound - required libraries not available")

def generate_lose_sound(file_path):
    """Generate a simple lose sound"""
    try:
        import numpy as np
        from scipy.io import wavfile
        
        # Generate a sad sound
        sample_rate = 44100
        t = np.linspace(0, 1.5, int(sample_rate * 1.5))
        sound = np.sin(2 * np.pi * 349.23 * t) * np.exp(-t*3)  # F4 note
        sound += 0.7 * np.sin(2 * np.pi * 277.18 * t) * np.exp(-t*3)  # C#4 note
        
        # Normalize to 16-bit range
        sound = np.int16(sound / np.max(np.abs(sound)) * 32767)
        
        # Write to file
        wavfile.write(file_path, sample_rate, sound)
        print(f"Generated lose sound at {file_path}")
    except ImportError:
        print("Could not generate lose sound - required libraries not available")

def print_hangman(attempts):
    """Print hangman ASCII art based on attempts left"""
    stages = [
        """
            ------
            |    |
            |
            |
            |
            |
        """,
        """
            ------
            |    |
            |    O
            |
            |
            |
        """,
        """
            ------
            |    |
            |    O
            |    |
            |
            |
        """,
        """
            ------
            |    |
            |    O
            |   /|
            |
            |
        """,
        """
            ------
            |    |
            |    O
            |   /|\
            |
            |
        """,
        """
            ------
            |    |
            |    O
            |   /|\
            |   /
            |
        """,
        """
            ------
            |    |
            |    O
            |   /|\
            |   / \
            |
        """
    ]
    idx = max(0, min(attempts, len(stages) - 1))
    print(stages[idx])

def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

if __name__ == "__main__":
    main()