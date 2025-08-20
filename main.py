def print_win_art():
    from images import WIN_ART
    print(WIN_ART)

def print_game_over_art():
    from images import GAME_OVER_ART
    print(GAME_OVER_ART)
import os
import random
import threading
import winsound
import unicodedata
import time
import sys
from images import HANGMAN_STAGES, WIN_ART, GAME_OVER_ART, YOU_LOSE_ART

# Color codes and helpers
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def color_text(text, color):
    return f"{color}{text}{Colors.RESET}"

def play_sound(sound_path):
    try:
        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception:
        pass
def print_win_art():
    print(WIN_ART)

def print_game_over_art():
    print(GAME_OVER_ART)
from settings import get_default_settings, get_language_strings
# ======================
# Settings Management
# ======================
def get_default_settings():
    return {
        'difficulty': '2',  # 1=Easy, 2=Normal, 3=Hard
        'category': None,   # None means random
        'mode': '1',        # 1=Single, 2=Multi
        'hint': True,       # Hint enabled by default
    }

def settings_menu(settings, categories, lang):
    print(f"\n{lang['settings_menu']}")
    print(f"1. {lang['difficulty']} ({lang['current']}: {{}}):".format({'1': lang['easy'], '2': lang['normal'], '3': lang['hard']}.get(settings['difficulty'], lang['normal'])))
    print(f"2. {lang['category']} ({lang['current']}: {{}})".format(settings['category'] if settings['category'] else lang['random'] if 'random' in lang else 'Random'))
    print(f"3. {lang['mode']} ({lang['current']}: {{}}):".format(lang['single_player'] if settings['mode']=='1' else lang['multiplayer']))
    print(f"4. {lang['hint']} ({lang['current']}: {{}}):".format(lang['activated'] if settings.get('hint', True) else lang['deactivated']))
    print(f"5. {lang['language']} ({lang['current']}: {settings.get('language', 'es')})")
    print(f"6. {lang['start']}")
    print(f"7. {lang['back']}")
    while True:
        choice = input(lang['select_setting'].format(max_opt=7)).strip()
        if choice == '1':
            print(lang['select_difficulty'])
            print(f"1. {lang['easy']}")
            print(f"2. {lang['normal']}")
            print(f"3. {lang['hard']}")
            d = input("1, 2, 3: ").strip()
            if d in {'1','2','3'}:
                settings['difficulty'] = d
                print(lang['difficulty'] + " " + lang['activated'].lower() + ".")
            else:
                print(lang['invalid_input'])
        elif choice == '2':
            print(lang['category'] + "s disponibles:")
            for idx, cat in enumerate(categories.keys(), 1):
                print(f"{idx}. {cat}")
            c = input(lang['choose_category']).strip()
            if c.isdigit() and 1 <= int(c) <= len(categories):
                settings['category'] = list(categories.keys())[int(c)-1]
            elif c == '':
                settings['category'] = None
            else:
                print(lang['invalid_input'])
        elif choice == '3':
            print(f"1. {lang['single_player']}\n2. {lang['multiplayer']}")
            m = input(lang['choose_mode']).strip()
            if m in {'1','2'}:
                settings['mode'] = m
            else:
                print(lang['invalid_input'])
        elif choice == '4':
            # Toggle hint setting
            print(lang['current_hint'].format(status=lang['activated'] if settings.get('hint', True) else lang['deactivated']))
            toggle = input(lang['activate_hint']).strip().lower()
            if toggle == 'a':
                settings['hint'] = True
                print(lang['hint_on'])
            elif toggle == 'd':
                settings['hint'] = False
                print(lang['hint_off'])
            else:
                print(lang['invalid_input'])
        elif choice == '5':
            # Change language
            new_lang = input(lang['choose_language']).strip().lower()
            if new_lang in ['es', 'en']:
                settings['language'] = new_lang
                print(lang['language_set'].format(lang=new_lang))
                return False  # To reload menu with new language
            else:
                print(lang['invalid_input'])
        elif choice == '6':
            iniciar_juego = True
            return iniciar_juego
        elif choice == '7':
            break
        else:
            print("Entrada inválida.")




def main():
    settings = get_default_settings()
    lang = get_language_strings(settings)
    print(color_text(lang['welcome'], Colors.CYAN))
    score = 0
    high_score = load_high_score()
    categories = load_categories()
    # Initial settings selection
    iniciar_juego = settings_menu(settings, categories, lang)
    if iniciar_juego:
        menu_choice = '1'
    else:
        menu_choice = ''
    while True:
        if not menu_choice:
            print(color_text(f"\n{lang['main_menu']}", Colors.YELLOW))
            print(f"1. {lang['start_game']}")
            print(f"2. {lang['settings']}")
            print(f"3. {lang['quit']}")
            menu_choice = input(lang['choose_option']).strip()
        if menu_choice == '2':
            iniciar_juego = settings_menu(settings, categories, lang)
            if iniciar_juego:
                menu_choice = '1'
                continue
            else:
                menu_choice = ''
                continue
        elif menu_choice == '3':
            print_game_over_art()
            print(f"{lang['final_score']}: {score}")
            break
        elif menu_choice == '1':
            # Play game
            if settings['mode'] == '2':
                word = input("Jugador 1, ingresa una palabra o frase para que el Jugador 2 adivine: ").strip()
                category = input("Ingresa una categoría para esta palabra/frase (opcional): ").strip()
                won = play_hangman(color_text, Colors, word, category, multiplayer=True, difficulty=settings['difficulty'], settings=settings)
            else:
                if settings['category']:
                    cat_name = settings['category']
                    word = random.choice(categories[cat_name])
                    category = cat_name
                else:
                    cat_name = random.choice(list(categories.keys()))
                    word = random.choice(categories[cat_name])
                    category = cat_name
                won = play_hangman(color_text, Colors, word, category, difficulty=settings['difficulty'], settings=settings)
            if won:
                score += 1
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                    print(color_text(lang['new_high_score'].format(score=high_score), Colors.CYAN))
            print(f"{lang['current_score']}: {score} | {lang['high_score']}: {high_score}")
            menu_choice = ''

def play_hangman(color_text, Colors, word, category=None, multiplayer=False, difficulty='2', settings=None):
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

    # Set attempts based on difficulty
    if difficulty == '1':
        attempts = 10
    elif difficulty == '2':
        attempts = 6
    elif difficulty == '3':
        attempts = 4
    else:
        attempts = 6

    word_lower = word.lower()
    max_attempts = attempts
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
    hint_enabled = settings.get('hint', True) if settings else True
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
            print_hangman(attempts, max_attempts)
            # Offer a hint after 3 wrong guesses, only once, if enabled
            if hint_enabled and wrong_guesses == 3 and not hint_used:
                # Reveal a random unguessed letter
                unguessed = [remove_accents(c.lower()) for c in word if c.isalnum() and remove_accents(c.lower()) not in guessed]
                if unguessed:
                    hint_letter = random.choice(unguessed)
                    guessed.add(hint_letter)
                    print(color_text(f"Pista: La palabra contiene la letra '{hint_letter}'.", Colors.CYAN))
                    hint_used = True
                else:
                    print(color_text("No hay más letras para revelar!", Colors.YELLOW))
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
    print_hangman(attempts, max_attempts)
    print(YOU_LOSE_ART)
    print(color_text(f"Game over! La Respuesta era: {word}", Colors.RED))
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

def print_hangman(attempts, max_attempts):
    """Print hangman ASCII art based on attempts left and max attempts"""
    wrong_guesses = max_attempts - attempts
    total_stages = len(HANGMAN_STAGES) - 1
    stage_idx = min(total_stages, max(0, int(round(wrong_guesses * total_stages / max(1, max_attempts)))))
    print(HANGMAN_STAGES[stage_idx])

def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

if __name__ == "__main__":
    main()