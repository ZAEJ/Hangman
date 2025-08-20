import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
import string
import os
import winsound
import unicodedata
import sys

# Path to your images (update if your folder is different)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

HANGMAN_IMAGES = [resource_path(f'images/stage{i}.png') for i in range(7)]
WIN_IMAGE = resource_path('images/win.png')
LOSE_IMAGE = resource_path('images/lose.png')
GAME_OVER_IMAGE = resource_path('images/gameover.png')

# --- Category and High Score helpers ---
def load_categories(language='es'):
    if language == 'en':
        words_path = resource_path("src/words_en.txt")
    else:
        words_path = resource_path("src/words_es.txt")
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

# --- Localization ---
LANGUAGES = {
    'en': {
        'settings': 'Settings',
        'difficulty': 'Difficulty',
        'category': 'Category',
        'mode': 'Mode',
        'hint': 'Hint',
        'enable_hint': 'Enable Hint',
        'save': 'Save',
        'random': 'Random',
        'single': 'Single',
        'multi': 'Multiplayer',
        'score': 'Score',
        'high_score': 'High Score',
        'restart': 'Restart Game',
        'guess': 'Guess a letter or phrase:',
        'guessed': 'Guessed',
        'unused': 'Unused',
        'category_label': 'Category',
        'win': 'Congratulations! You guessed the phrase:',
        'lose': 'You lose! The word was:',
        'wrong_guess': "Wrong guess:",
        'good_guess': "Good guess:",
        'already_guessed': "You already guessed that character.",
        'enter_guess': "Please enter a guess.",
        'wrong_phrase': "Wrong phrase guess.",
        'hint_msg': "Hint: The word contains the letter",
        'no_more_letters': "No more letters to reveal!",
        'new_high_score': "New High Score!",
        'language': 'Language',
    },
    'es': {
        'settings': 'Configuración',
        'difficulty': 'Dificultad',
        'category': 'Categoría',
        'mode': 'Modo',
        'hint': 'Pista',
        'enable_hint': 'Activar pista',
        'save': 'Guardar',
        'random': 'Aleatorio',
        'single': 'Individual',
        'multi': 'Multijugador',
        'score': 'Puntaje',
        'high_score': 'Récord',
        'restart': 'Reiniciar Juego',
        'guess': 'Adivina una letra o frase:',
        'guessed': 'Adivinadas',
        'unused': 'Sin usar',
        'category_label': 'Categoría',
        'win': '¡Felicidades! Adivinaste la frase:',
        'lose': '¡Perdiste! La palabra era:',
        'wrong_guess': "Letra incorrecta:",
        'good_guess': "¡Bien! Letra:",
        'already_guessed': "Ya adivinaste ese carácter.",
        'enter_guess': "Por favor ingresa una letra o frase.",
        'wrong_phrase': "Frase incorrecta.",
        'hint_msg': "Pista: La palabra contiene la letra",
        'no_more_letters': "¡No hay más letras para revelar!",
        'new_high_score': "¡Nuevo récord!",
        'language': 'Idioma',
    }
}

class HangmanGUI:
    def play_sound(self, sound_path):
        try:
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass
    def setup_sounds(self):
        self.win_sound = resource_path('src/sounds/win2.wav')
        self.lose_sound = resource_path('src/sounds/lose.wav')
        self.gameover_sound = resource_path('src/sounds/game_over.wav')
    def get_font(self, size=18, weight="normal"):
        # Comic Sans MS is playful and widely available on Windows
        return ("Comic Sans MS", size, weight)
    def load_images(self):
        self.hangman_imgs = [ImageTk.PhotoImage(Image.open(img)) for img in HANGMAN_IMAGES]
        self.win_img = ImageTk.PhotoImage(Image.open(WIN_IMAGE))
        self.lose_img = ImageTk.PhotoImage(Image.open(LOSE_IMAGE))
        self.gameover_img = ImageTk.PhotoImage(Image.open(GAME_OVER_IMAGE))

    def get_default_settings(self):
        return {
            'difficulty': '2',  # 1=Easy, 2=Normal, 3=Hard
            'category': None,   # None means random
            'mode': '1',        # 1=Single, 2=Multi
            'hint': True,       # Hint enabled by default
        }

    def __init__(self, root):
        self.root = root
        self.language = 'es'
        self.lang = LANGUAGES[self.language]
        self.root.title('Hangman Game')
        self.root.geometry('1000x700')  # Start larger, but allow resizing
        self.root.minsize(800, 600)
        self.categories = load_categories(self.language)
        self.settings = self.get_default_settings()
        self.score = 0
        self.high_score = load_high_score()
        self.load_images()
        self.setup_widgets()
        self.setup_sounds()
        self.start_new_game()

    # Removed broken duplicate setup_widgets

    def setup_widgets(self):
        # Main frame must be created first
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill='both', padx=0, pady=0)
        for i in range(8):
            self.main_frame.rowconfigure(i, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Message variable and label (for win/lose/status messages)
        self.msg_var = tk.StringVar()
        self.msg_label = tk.Label(self.main_frame, textvariable=self.msg_var, font=self.get_font(14), fg="blue")
        self.msg_label.grid(row=5, column=0, pady=(8, 0), sticky='n')

        # Entry frame for guesses
        entry_frame = tk.Frame(self.main_frame)
        entry_frame.grid(row=3, column=0, pady=(8, 0), sticky='ew', padx=10)
        entry_frame.columnconfigure(1, weight=1)
        self.guess_label = tk.Label(entry_frame, text=self.lang['guess'], font=self.get_font(14))
        self.guess_label.grid(row=0, column=0, sticky='w')
        self.guess_entry = tk.Entry(entry_frame, width=16, font=self.get_font(18))
        self.guess_entry.grid(row=0, column=1, sticky='ew', padx=4)
        self.submit_btn = tk.Button(entry_frame, text="Submit", font=self.get_font(12), command=self.submit_guess)
        self.submit_btn.grid(row=0, column=2, padx=8)
        self.guess_entry.bind('<Return>', lambda event: self.submit_guess())

        # Letter buttons
        self.letters_frame = tk.Frame(self.main_frame)
        self.letters_frame.grid(row=4, column=0, pady=(4, 0), sticky='ew', padx=4)
        self.letter_buttons = {}
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for i, letter in enumerate(letters):
            btn = tk.Button(
                self.letters_frame,
                text=letter,
                width=2, height=1,
                font=self.get_font(12, "bold"),
                command=lambda l=letter: self.letter_button_guess(l)
            )
            btn.grid(row=i//12, column=i%12, padx=1, pady=1, sticky='nsew')
            self.letter_buttons[letter] = btn
        for i in range(12):
            self.letters_frame.columnconfigure(i, weight=1, minsize=18)
        for i in range(4):
            self.letters_frame.rowconfigure(i, weight=1, minsize=18)

        self.img_label = tk.Label(self.main_frame)
        self.img_label.grid(row=0, column=0, pady=(10, 0), sticky='n')

        self.category_var = tk.StringVar()
        self.category_label = tk.Label(self.main_frame, textvariable=self.category_var, font=self.get_font(14), fg="navy")
        self.category_label.grid(row=1, column=0, pady=(6, 0), sticky='n')

        self.word_var = tk.StringVar()
        self.word_label = tk.Label(self.main_frame, textvariable=self.word_var, font=self.get_font(28, "bold"))
        self.word_label.grid(row=2, column=0, pady=(12, 0), sticky='n')

        self.guessed_var = tk.StringVar()
        self.guessed_label = tk.Label(self.main_frame, textvariable=self.guessed_var, font=self.get_font(10), fg="darkgreen")
        self.guessed_label.grid(row=6, column=0, pady=(2, 0), sticky='n')
        self.unused_var = tk.StringVar()
        self.unused_label = tk.Label(self.main_frame, textvariable=self.unused_var, font=self.get_font(10), fg="darkred")
        self.unused_label.grid(row=7, column=0, pady=(2, 0), sticky='n')

        # Top bar: score left, settings right
        topbar = tk.Frame(self.root)
        topbar.pack(side=tk.TOP, fill='x')
        self.score_var = tk.StringVar()

        self.score_label = tk.Label(topbar, textvariable=self.score_var, font=self.get_font(12), fg="purple")
        self.score_label.pack(side=tk.LEFT, padx=12, pady=8)

        # Frame for settings and restart buttons (stacked vertically, top right)
        self.topright_frame = tk.Frame(topbar)
        self.topright_frame.pack(side=tk.RIGHT, padx=12, pady=8, anchor='ne')
        self.settings_btn = tk.Button(self.topright_frame, text=self.lang['settings'], font=self.get_font(12), command=self.open_settings)
        self.settings_btn.pack(side=tk.TOP, fill='x', pady=(0, 4))
        self.restart_btn = tk.Button(self.topright_frame, text=self.lang['restart'], font=self.get_font(12), command=self.start_new_game)
        self.restart_btn.pack(side=tk.TOP, fill='x')

    # ...existing code...

    # ...existing code...

    # Remove restart button from main_frame (now in top right)

    def letter_button_guess(self, letter):
        if self.guess_entry['state'] == tk.NORMAL:
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.insert(0, letter)
            self.submit_guess()

    def update_score_display(self):
        self.score_var.set(f"{self.lang['score']}: {self.score} | {self.lang['high_score']}: {self.high_score}")

    def open_settings(self):
        s = self.settings
        dlg = tk.Toplevel(self.root)
        dlg.title(self.lang['settings'])
        # Add a frame with minimal padding for settings
        frame = tk.Frame(dlg, padx=10, pady=10)
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text=self.lang['difficulty']+':').grid(row=0, column=0, sticky='w')
        diff_var = tk.StringVar(value=s['difficulty'])
        tk.OptionMenu(frame, diff_var, '1', '2', '3').grid(row=0, column=1)
        tk.Label(frame, text=self.lang['category']+':').grid(row=1, column=0, sticky='w')
        cat_var = tk.StringVar(value=s['category'] or self.lang['random'])
        cat_choices = [self.lang['random']] + list(self.categories.keys())
        tk.OptionMenu(frame, cat_var, *cat_choices).grid(row=1, column=1)
        tk.Label(frame, text=self.lang['mode']+':').grid(row=2, column=0, sticky='w')
        mode_var = tk.StringVar(value=s['mode'])
        tk.OptionMenu(frame, mode_var, '1', '2').grid(row=2, column=1)
        tk.Label(frame, text=self.lang['hint']+':').grid(row=3, column=0, sticky='w')
        hint_var = tk.BooleanVar(value=s['hint'])
        tk.Checkbutton(frame, variable=hint_var, text=self.lang['enable_hint']).grid(row=3, column=1, sticky='w')
        tk.Label(frame, text=self.lang['language']+':').grid(row=4, column=0, sticky='w')
        lang_var = tk.StringVar(value=self.language)
        tk.OptionMenu(frame, lang_var, *LANGUAGES.keys()).grid(row=4, column=1)
        def save_and_close():
            s['difficulty'] = diff_var.get()
            cat = cat_var.get()
            s['category'] = None if cat == self.lang['random'] else cat
            s['mode'] = mode_var.get()
            s['hint'] = hint_var.get()
            # If language changed, reload categories
            if lang_var.get() != self.language:
                self.language = lang_var.get()
                self.lang = LANGUAGES[self.language]
                self.categories = load_categories(self.language)
            self.set_language(self.language)
            dlg.destroy()
        tk.Button(frame, text=self.lang['save'], command=save_and_close).grid(row=5, column=0, columnspan=2, pady=8)

    def _test_win(self):
        self.msg_var.set("Congratulations! You win! (Test)")
        self.img_label.config(image=self.win_img)
        self.play_sound(self.win_sound)
        self.disable_input()

    def _test_lose(self):
        self.msg_var.set(f"You lose! The word was: {self.word} (Test)")
        self.img_label.config(image=self.lose_img)
        self.play_sound(self.lose_sound)
        self.disable_input()

    def _test_gameover(self):
        self.msg_var.set("Game Over! (Test)")
        self.img_label.config(image=self.gameover_img)
        self.play_sound(self.gameover_sound)
        self.disable_input()

    def start_new_game(self):
        # If a game is in progress and not already lost/won, count as a loss
        if hasattr(self, 'attempts_left') and self.attempts_left > 0:
            if not all((self.remove_accents(c.upper()) in self.guessed or not c.isalnum()) for c in self.word):
                # Only count as loss if not already won
                self.msg_var.set(f"{self.lang['lose']} {self.word} (Reiniciado)")
                self.img_label.config(image=self.lose_img)
                self.play_sound(self.lose_sound)
                self.score = 0
                self.update_score_display()
        # Select word and category based on settings
        s = self.settings
        if s['mode'] == '2':
            # Multiplayer: ask for word and category
            word = simpledialog.askstring("Multiplayer", "Player 1: Enter a word or phrase for Player 2 to guess:")
            if not word:
                word = random.choice(random.choice(list(self.categories.values())))
            category = simpledialog.askstring("Multiplayer", "Enter a category for this word/phrase (optional):")
            if not category:
                category = "Custom"
        else:
            if s['category']:
                cat_name = s['category']
                word = random.choice(self.categories[cat_name])
                category = cat_name
            else:
                cat_name = random.choice(list(self.categories.keys()))
                word = random.choice(self.categories[cat_name])
                category = cat_name
        self.word = word.upper()
        self.category = category
        self.guessed = set()
        self.guessed_display = set()
        self.hint_used = False
        self.hint_enabled = s.get('hint', True)
        # Set attempts based on difficulty
        if s['difficulty'] == '1':
            self.max_attempts = 10
        elif s['difficulty'] == '2':
            self.max_attempts = 6
        elif s['difficulty'] == '3':
            self.max_attempts = 4
        else:
            self.max_attempts = 6
        self.attempts_left = self.max_attempts
        self.stage = 0
        self.img_label.config(image=self.hangman_imgs[self.stage])
        self.update_word_display()
        self.guess_entry.config(state=tk.NORMAL)
        self.submit_btn.config(state=tk.NORMAL)
        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL)
        self.msg_var.set("")
        self.category_var.set(f"{self.lang['category_label']}: {self.category}")
        self.update_score_display()
        self.guess_entry.focus_set()

    def remove_accents(self, input_str):
        return ''.join(
            c for c in unicodedata.normalize('NFD', input_str)
            if unicodedata.category(c) != 'Mn'
        )

    def update_word_display(self):
        display = ' '.join([
            c if (self.remove_accents(c.upper()) in self.guessed or not c.isalnum()) else '_'
            for c in self.word
        ])
        self.word_var.set(display)
        # Update guessed and unused letters
        all_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        guessed_display_noacc = set(self.remove_accents(g.upper()) for g in self.guessed_display)
        unused = all_letters - guessed_display_noacc
        self.guessed_var.set(f"{self.lang['guessed']}: {' '.join(sorted(self.guessed_display)) if self.guessed_display else '-'}")
        self.unused_var.set(f"{self.lang['unused']}: {' '.join(sorted(unused))}")
        # Update letter buttons
        for letter, btn in self.letter_buttons.items():
            if letter in self.guessed_display:
                btn.config(state=tk.DISABLED)
            else:
                btn.config(state=tk.NORMAL)

    def submit_guess(self):
        guess = self.guess_entry.get().strip().upper()
        self.guess_entry.delete(0, tk.END)
        if not guess:
            self.msg_var.set(self.lang["enter_guess"])
            return
        # Phrase guess
        if len(guess) > 1:
            guess_no_acc = self.remove_accents(guess)
            word_no_acc = self.remove_accents(self.word)
            if guess_no_acc == word_no_acc:
                self.guessed.update([self.remove_accents(c.upper()) for c in self.word if c.isalnum()])
                self.update_word_display()
                self.msg_var.set(f"{self.lang['win']} {self.word}")
                self.img_label.config(image=self.win_img)
                self.play_sound(self.win_sound)
                self.disable_input()
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                    save_high_score(self.high_score)
                    messagebox.showinfo(self.lang["new_high_score"], f"New High Score: {self.high_score}")
                self.update_score_display()
                return
            else:
                self.attempts_left -= 1
                self.stage = self.max_attempts - self.attempts_left
                self.img_label.config(image=self.hangman_imgs[self.stage])
                self.msg_var.set(self.lang["wrong_phrase"])
                self.update_word_display()
                self.check_game_over()
                return
        # Single letter guess
        if len(guess) != 1 or not guess.isalnum():
            self.msg_var.set("Enter a single letter or the whole phrase.")
            return
        guess_no_acc = self.remove_accents(guess)
        if guess_no_acc in self.guessed or guess in self.guessed_display:
            self.msg_var.set(self.lang['already_guessed'])
            return
        self.guessed_display.add(guess)
        word_noacc_set = set(self.remove_accents(c.upper()) for c in self.word if c != ' ')
        if guess_no_acc in word_noacc_set:
            self.guessed.add(guess_no_acc)
            self.msg_var.set(f"{self.lang['good_guess']}: '{guess}'!")
        else:
            self.attempts_left -= 1
            self.stage = self.max_attempts - self.attempts_left
            self.img_label.config(image=self.hangman_imgs[self.stage])
            self.msg_var.set(f"{self.lang['wrong_guess']} '{guess}'. Attempts left: {self.attempts_left}")
            # Offer a hint after 3 wrong guesses, only once, if enabled
            wrong_guesses = self.max_attempts - self.attempts_left
            if self.hint_enabled and wrong_guesses == 3 and not self.hint_used:
                unguessed = [self.remove_accents(c.upper()) for c in self.word if c.isalnum() and self.remove_accents(c.upper()) not in self.guessed]
                if unguessed:
                    hint_letter = random.choice(unguessed)
                    self.guessed.add(hint_letter)
                    self.msg_var.set(f"{self.lang['hint_msg']} '{hint_letter}'.")
                    self.hint_used = True
                else:
                    self.msg_var.set(self.lang["no_more_letters"])
                    self.hint_used = True
        self.update_word_display()
        self.check_game_over()

    def check_game_over(self):
        if all((self.remove_accents(c.upper()) in self.guessed or not c.isalnum()) for c in self.word):
            self.msg_var.set(f"{self.lang['win']} {self.word}")
            self.img_label.config(image=self.win_img)
            self.play_sound(self.win_sound)
            self.disable_input()
            self.restart_btn.config(state=tk.NORMAL)
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                save_high_score(self.high_score)
                import tkinter.messagebox as messagebox
                messagebox.showinfo(self.lang['new_high_score'], f"{self.lang['new_high_score']}: {self.high_score}")
            self.update_score_display()
        elif self.attempts_left == 0:
            self.msg_var.set(f"{self.lang['lose']} {self.word}")
            self.img_label.config(image=self.lose_img)
            self.play_sound(self.lose_sound)
            self.disable_input()
            self.restart_btn.config(state=tk.NORMAL)
            self.score = 0
            self.update_score_display()

    def disable_input(self):
        self.guess_entry.config(state=tk.DISABLED)
        self.submit_btn.config(state=tk.DISABLED)
        for btn in self.letter_buttons.values():
            btn.config(state=tk.DISABLED)
        # Ensure restart button is always enabled
        self.restart_btn.config(state=tk.NORMAL)

if __name__ == '__main__':
    try:
        root = tk.Tk()
        app = HangmanGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print('Error starting Hangman GUI:')
        traceback.print_exc()
