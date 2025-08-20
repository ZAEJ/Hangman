import random
import winsound
import os
import unicodedata
import time
import sys

def main():
    print("Welcome to my Python project!")
    play_hangman()

def play_hangman():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        words_path = os.path.join(base_dir, "src", "words.txt")
        print(f"Loading words from: {words_path}")
        
        with open(words_path, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
            
        if not words:
            raise ValueError("words.txt is empty!")
    except Exception as e:
        print(f"\n⚠️ Could not load words.txt:\n{e}")
        print("Using default word list instead.\n")
        words = ["python", "hangman", "challenge", "programming", "bootcamp"]
    
    # Create sounds directory if it doesn't exist
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sounds_dir = os.path.join(base_dir, 'src', 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Generate sounds if they don't exist
    win_path = os.path.join(sounds_dir, 'win2.wav')
    game_over_path = os.path.join(sounds_dir, 'game_over.wav')
    lose_path = os.path.join(sounds_dir, 'lose.wav')
    
    if not os.path.exists(win_path):
        print("Generating win sound...")
        generate_win_sound(win_path)
    
    if not os.path.exists(game_over_path):
        print("Generating game over sound...")
        generate_game_over_sound(game_over_path)
    
    if not os.path.exists(lose_path):
        print("Generating lose sound...")
        generate_lose_sound(lose_path)
    
    # Pick a random word or phrase
    word = random.choice(words)
    word_lower = word.lower()
    guessed = set()
    attempts = 6
    
    print("\nLet's play Hangman!")
    
    def display_word():
        return ' '.join([
            letter if (letter.lower() in guessed or not letter.isalnum()) else '_'
            for letter in word
        ])
    
    while attempts > 0:
        print(f"\nWord: {display_word()}")
        print(f"Attempts left: {attempts}")
        guess = input("Guess a letter, number, or the whole phrase: ").strip().lower()
        
        if not guess:
            print("Please enter a guess.")
            continue
        
        # Guessing the whole phrase
        if len(guess) > 1:
            if guess == word_lower:
                guessed.update([c.lower() for c in word if c.isalnum()])
                print(f"Congratulations! You guessed the phrase: {word}")
                time.sleep(0.5)
                #print(f"Trying to play: {win_path}")
                play_sound(win_path)
                time.sleep(0.5)
                # play_sound(game_over_path)
                break
            else:
                attempts -= 1
                print("Wrong phrase guess.")
                continue
        
        # Guessing a single character
        if len(guess) != 1:
            print("Please enter a single character or the whole phrase.")
            continue
        
        if guess in guessed:
            print("You already guessed that character.")
            continue
        
        if guess in [c.lower() for c in word if c != ' ']:
            guessed.add(guess)
            print("Good guess!")
        else:
            attempts -= 1
            print("Wrong guess.")
            print_hangman(attempts)
        
        # Check if all alphanumeric characters have been guessed
        if all((c.lower() in guessed or not c.isalnum()) for c in word):
            print(f"\nCongratulations! You guessed the phrase: {word}")
            time.sleep(0.5)
            #print(f"Trying to play: {win_path}")
            play_sound(win_path)
            time.sleep(0.5)
            # play_sound(game_over_path)
            break
    
    if attempts <= 0:
        print_hangman(attempts)
        print(f"Game over! The phrase was: {word}")
        play_sound(lose_path)
        play_sound(game_over_path)

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
    print(stages[attempts])

def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

if __name__ == "__main__":
    main()