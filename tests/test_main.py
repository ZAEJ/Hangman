import random
import winsound
import os
import unicodedata

def main():
    print("Welcome to my Python project!")
    play_hangman()

def example_function(param):
    return f"Hello, {param}!"

def play_hangman():
    try:
        # Always resolve path relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        words_path = os.path.join(base_dir, "src", "words.txt")

        print(f"Loading words from: {words_path}")  # Debugging info

        # Read all non-empty lines
        with open(words_path, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]

        if not words:
            raise ValueError("words.txt is empty!")

    except Exception as e:
        # Detailed error message for debugging
        print(f"\n⚠️ Could not load words.txt:\n{e}")
        print("Using default word list instead.\n")
        words = ["python", "hangman", "challenge", "programming", "bootcamp"]

    # Pick a random word or phrase
    word = random.choice(words)
    word_lower = word.lower()
    guessed = set()
    attempts = 6

    print("\nLet's play Hangman!")

    def display_word():
        # Show special characters and spaces, hide only alphanumeric
        return ' '.join([
            letter if (letter.lower() in guessed or not letter.isalnum()) else '_' for letter in word
        ])

    while attempts > 0:
        print(f"\nWord: {display_word()}")
        print(f"Attempts left: {attempts}")
        guess = input("Guess a letter, number, or the whole phrase: ").strip().lower()

        if not guess:
            print("Please enter a guess.")
            continue

        # Guessing the whole phrase (case-insensitive, spaces and special characters allowed)
        if len(guess) > 1:
            if guess == word_lower:
                guessed.update([c.lower() for c in word if c.isalnum()])
                print(f"Congratulations! You guessed the phrase: {word}")
                # Play win and game over sounds
                base_dir = os.path.dirname(os.path.abspath(__file__))
                win_path = os.path.join(base_dir, 'src', 'sounds', 'win.wav')
                game_over_path = os.path.join(base_dir, 'src', 'sounds', 'game_over.wav')
                print("Playing win sound") #Temporary print for debugging
                winsound.PlaySound(win_path, winsound.SND_FILENAME)
                print("Playing game over sound") #Temporary print for debugging
                winsound.PlaySound(game_over_path, winsound.SND_FILENAME)
                break
            else:
                attempts -= 1
                print("Wrong phrase guess.")
                continue

        # Guessing a single character (letter, number, or special character)
        if len(guess) != 1:
            print("Please enter a single character or the whole phrase.")
            continue

        # Accept any visible character, but only add to guessed if it's in the word (case-insensitive)
        if guess in guessed:
            print("You already guessed that character.")
            continue

        if guess in [c.lower() for c in word if c != ' ']:
            guessed.add(guess)
            print("Good guess!")
        else:
            attempts -= 1
            print("Wrong guess.")

        # Check if all alphanumeric characters have been guessed
        if all((c.lower() in guessed or not c.isalnum()) for c in word):
            print(f"\nCongratulations! You guessed the phrase: {word}")
            # Play win and game over sounds
            base_dir = os.path.dirname(os.path.abspath(__file__))
            win_path = os.path.join(base_dir, 'src', 'sounds', 'win.wav')
            game_over_path = os.path.join(base_dir, 'src', 'sounds', 'game_over.wav')
            print("Playing win sound") #Temporary print for debugging
            winsound.PlaySound(win_path, winsound.SND_FILENAME)
            print("Playing game over sound") #Temporary print for debugging
            winsound.PlaySound(game_over_path, winsound.SND_FILENAME)
            break

    else:
        print("""
  _______
 |/      |
 |      (_)
 |      \|/
 |       |
 |      / \\
 |
_|___
        """)
    print(f"Game over! The phrase was: {word}")
    # Play lose sound
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lose_path = os.path.join(base_dir, 'src', 'sounds', 'lose.wav')
    game_over_path = os.path.join(base_dir, 'src', 'sounds', 'game_over.wav')
    winsound.PlaySound(lose_path, winsound.SND_FILENAME)
    winsound.PlaySound(game_over_path, winsound.SND_FILENAME)

def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

if __name__ == "__main__":
    main()
