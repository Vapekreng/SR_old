from bearlibterminal import terminal

import localization as lk
from keyset import keyset
from settings import settings
import adventure
import menu_controls
import config
import menu_settings

SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT
MAIN_MENU_LEFT_UPPER_CONER = [35, 15]
NORMAL_TEXT_COLOR = 'white'
LIGHTED_TEXT_COLOR = 'dark yellow'


class Buttons:

    def __init__(self, names, press_button):
        self.names = names
        self.press_button = press_button

    def get_name(self):
        language = settings.language
        name = self.names[language]
        return name

    def press(self):
        self.press_button()


class MainMenu:

    def __init__(self):
        self.time_to_quit = False
        self.buttons = self.get_buttons()
        self.navigation_codes = self.get_navigation_codes()
        self.navigation_actions = [self._prev_button, self._next_button, self._press_button, self._set_quit,
                                   self._set_quit, self._prev_button, self._next_button]
        self.length = len(self.buttons)
        self.position = 0

    def get_buttons(self):
        buttons = []
        buttons.append(Buttons(lk.NEW_GAME, adventure.new_game))
        buttons.append(Buttons(lk.LOAD_GAME, adventure.load_game))
        buttons.append(Buttons(lk.CONTROLS, menu_controls.main_loop))
        buttons.append(Buttons(lk.SETTINGS, menu_settings.main_loop))
        buttons.append(Buttons(lk.EXIT, self._set_quit))
        return buttons

    def get_navigation_codes(self):
        codes = [keyset.codes['up'], keyset.codes['down'], terminal.TK_ENTER, terminal.TK_ESCAPE, terminal.TK_CLOSE,
                 terminal.TK_UP, terminal.TK_DOWN]
        return codes

    def refresh(self):
        self.buttons = self.get_buttons()
        self.navigation_codes = self.get_navigation_codes()

    def print(self):
        length = self.length
        for position in range(length):
            self._print_button(position)
        terminal.refresh()

    def key_processing(self):
        code = terminal.read()
        if code in self.navigation_codes:
            index = self.navigation_codes.index(code)
            self.navigation_actions[index]()

    def _print_button(self, position):
        current_button = self.buttons[position]
        text = current_button.get_name()
        x = MAIN_MENU_LEFT_UPPER_CONER[0]
        y = MAIN_MENU_LEFT_UPPER_CONER[1] + position
        if self.position == position:
            terminal.color(LIGHTED_TEXT_COLOR)
        terminal.printf(x, y, text)
        terminal.color(NORMAL_TEXT_COLOR)

    def _set_quit(self):
        self.time_to_quit = True

    def _press_button(self):
        position = self.position
        current_button = self.buttons[position]
        current_button.press()

    def _next_button(self):
        new_position = (self.position + 1) % self.length
        self.position = new_position

    def _prev_button(self):
        new_position = (self.position - 1) % self.length
        self.position = new_position


def main_loop():
    main_menu = MainMenu()
    while not main_menu.time_to_quit:
        main_menu.print()
        main_menu.key_processing()
        main_menu.refresh()

