# settings.py

SETTINGS_DEFAULTS = {
    'difficulty': '2',  # 1=Easy, 2=Normal, 3=Hard
    'category': None,   # None means random
    'mode': '1',        # 1=Single, 2=Multi
    'hint': True,       # Hint enabled by default
    'language': 'es',   # 'es' for Spanish, 'en' for English
}

LANGUAGES = {
    'es': {
        'welcome': "¡Bienvenido a mi proyecto de Python!",
        'main_menu': "Menú Principal:",
        'start_game': "Iniciar Juego",
        'settings': "Configuración",
        'quit': "Salir",
        'choose_option': "Elige una opción: ",
        'settings_menu': "Menú de Configuración:",
        'difficulty': "Dificultad",
        'category': "Categoría",
        'mode': "Modo de Juego",
        'hint': "Pista",
        'language': "Idioma",
        'back': "Volver al menú principal",
        'single_player': "Un jugador",
        'multiplayer': "Multijugador",
        'current': "actual",
        'activated': "Activada",
        'deactivated': "Desactivada",
        'start': "Iniciar Juego",
        'final_score': "Puntaje final",
        'current_score': "Puntaje actual",
        'high_score': "Puntaje más alto",
        'new_high_score': "¡Nuevo puntaje más alto: {score}!",
        'invalid_input': "Entrada inválida.",
        'select_setting': "Selecciona la opción a cambiar (1-{max_opt}): ",
        'select_difficulty': "Selecciona la dificultad:",
        'easy': "Fácil (10 intentos)",
        'normal': "Normal (6 intentos)",
        'hard': "Difícil (4 intentos)",
        'choose_category': "Elige una categoría por número o presiona Enter para aleatoria: ",
        'choose_mode': "Elige el modo: ",
        'activate_hint': "¿Quieres activar o desactivar la pista? (a/d): ",
        'hint_on': "Pista activada.",
        'hint_off': "Pista desactivada.",
        'current_hint': "La pista está actualmente {status}.",
        'choose_language': "Elige el idioma (es/en): ",
        'language_set': "Idioma actualizado a {lang}.",
    },
    'en': {
        'welcome': "Welcome to my Python project!",
        'main_menu': "Main Menu:",
        'start_game': "Start Game",
        'settings': "Settings",
        'quit': "Quit",
        'choose_option': "Choose an option: ",
        'settings_menu': "Settings Menu:",
        'difficulty': "Difficulty",
        'category': "Category",
        'mode': "Game Mode",
        'hint': "Hint",
        'language': "Language",
        'back': "Back to main menu",
        'single_player': "Single Player",
        'multiplayer': "Multiplayer",
        'current': "current",
        'activated': "Activated",
        'deactivated': "Deactivated",
        'start': "Start Game",
        'final_score': "Final score",
        'current_score': "Current score",
        'high_score': "High score",
        'new_high_score': "New High Score: {score}!",
        'invalid_input': "Invalid input.",
        'select_setting': "Select setting to change (1-{max_opt}): ",
        'select_difficulty': "Select difficulty:",
        'easy': "Easy (10 attempts)",
        'normal': "Normal (6 attempts)",
        'hard': "Hard (4 attempts)",
        'choose_category': "Choose a category by number or press Enter for random: ",
        'choose_mode': "Choose mode: ",
        'activate_hint': "Do you want to activate or deactivate the hint? (a/d): ",
        'hint_on': "Hint activated.",
        'hint_off': "Hint deactivated.",
        'current_hint': "Hint is currently {status}.",
        'choose_language': "Choose language (es/en): ",
        'language_set': "Language set to {lang}.",
    }
}

def get_default_settings():
    return SETTINGS_DEFAULTS.copy()

def get_language_strings(settings):
    lang = settings.get('language', 'es')
    return LANGUAGES.get(lang, LANGUAGES['es'])
