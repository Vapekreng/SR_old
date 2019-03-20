from bearlibterminal import terminal

from keyset import keyset
import config
import localization as lk
from settings import settings

INVITE_TO_PRINT = '<<< ??? >>>'
TERMINAL_COLOR_NORMAL = 'white'
TERMINAL_COLOR_LIGHTED = 'yellow'
CAPTION_START_POSITION = [0, 1]
CAPTION_BORDER_POSITION = [0, 2]
CAPTION_NAME = 'Control settings'
BORDER_SYMBOL = '-'
LEFT_COLUMN_START_POSITION = [10, 4]
RIGHT_COLUMN_START_POSITION = [config.SCREEN_WIDTH // 2 + 1, 4]
RIGHT_COLUMN_WIDTH = config.SCREEN_WIDTH // 2


class Buttons:

    def __init__(self, comand_names, code):
        self.code = code
        self.names = comand_names

    def get_name(self):
        language = settings.language
        name = self.names[language]
        return name

    def get_key(self):
        key = keyset.keys[self.code]
        return key

    def get_code(self):
        return self.code


class MenuControls:

    def __init__(self):
        self.position = 0
        self.navigation_codes = self.get_navigation_codes()
        self.navigation_actions = [self._prev_button, self._next_button, self._press_button, self._set_quit, self._set_quit,
                                   self._prev_button, self._next_button]
        self.time_to_quit = False
        self.buttons = self.get_buttons()
        self.length = len(self.buttons)

    def get_buttons(self):
        buttons = []
        buttons.append(Buttons(lk.LEFT, keyset.codes['left']))
        buttons.append(Buttons(lk.UP, keyset.codes['up']))
        buttons.append(Buttons(lk.RIGHT, keyset.codes['right']))
        buttons.append(Buttons(lk.DOWN, keyset.codes['down']))
        buttons.append(Buttons(lk.UL, keyset.codes['ul']))
        buttons.append(Buttons(lk.UR, keyset.codes['ur']))
        buttons.append(Buttons(lk.DL, keyset.codes['dl']))
        buttons.append(Buttons(lk.DR, keyset.codes['dr']))
        return buttons

    def get_navigation_codes(self):
        codes = [keyset.codes['up'], keyset.codes['down'], terminal.TK_ENTER, terminal.TK_ESCAPE, terminal.TK_CLOSE,
                 terminal.TK_UP, terminal.TK_DOWN]
        return codes

    def _set_quit(self):
        self.time_to_quit = True

    def _prev_button(self):
        new_position = (self.position - 1) % self.length
        self.position = new_position

    def _next_button(self):
        new_position = (self.position + 1) % self.length
        self.position = new_position

    def key_processing(self):
        code = terminal.read()
        if code in self.navigation_codes:
            index = self.navigation_codes.index(code)
            self.navigation_actions[index]()

    def _press_button(self):
        self._print_invite_to_change_key()
        old_code = self.buttons[self.position].get_code()
        new_code = terminal.read()
        text = keyset.change_code(old_code, new_code)
        if (text in lk.WRONG_KEY) or (text in lk.KEY_IS_BUSY):
            self.print_error_message(text)
        else:
            self.navigation_codes = self.get_navigation_codes()
            self.buttons = self.get_buttons()

    def _print_invite_to_change_key(self):
        x, y = RIGHT_COLUMN_START_POSITION
        y = y + self.position
        text = INVITE_TO_PRINT.center(config.SCREEN_WIDTH // 2)
        terminal.color(TERMINAL_COLOR_LIGHTED)
        terminal.printf(x, y, text)
        terminal.color(TERMINAL_COLOR_NORMAL)
        terminal.refresh()

    def print_error_message(self, message_text):
        x, y = RIGHT_COLUMN_START_POSITION
        y = y + self.position
        text = message_text.center(config.SCREEN_WIDTH // 2)
        terminal.color(TERMINAL_COLOR_LIGHTED)
        terminal.printf(x, y, text)
        terminal.color(TERMINAL_COLOR_NORMAL)
        terminal.refresh()
        terminal.read()

    def _print_button(self, index):
        if index == self.position:
            terminal.color(TERMINAL_COLOR_LIGHTED)
        self._print_left_part(index)
        self._print_right_part(index)
        terminal.color(TERMINAL_COLOR_NORMAL)

    def _print_left_part(self, index):
        x0, y0 = LEFT_COLUMN_START_POSITION
        x = x0
        y = y0 + index
        text = self.buttons[index].get_name()
        terminal.printf(x, y, text)

    def _print_right_part(self, index):
        x0, y0 = RIGHT_COLUMN_START_POSITION
        x = x0
        y = y0 + index
        code = self.buttons[index].code
        key = keyset.keys[code]
        normalized_key = key.center(RIGHT_COLUMN_WIDTH)
        terminal.printf(x, y, normalized_key)

    def print(self):
        for i in range(self.length):
            self._print_button(i)
        terminal.refresh()

    @staticmethod
    def print_caption():
        x0, y0 = CAPTION_START_POSITION
        language = settings.language
        text = lk.CONTROL_SETTINGS[language]
        normalized_text = text.center(config.SCREEN_WIDTH)
        terminal.printf(x0, y0, normalized_text)
        x0, y0 = CAPTION_BORDER_POSITION
        border = BORDER_SYMBOL * config.SCREEN_WIDTH
        terminal.printf(x0, y0, border)
        terminal.refresh()


def main_loop():
    terminal.clear()
    menu = MenuControls()
    menu.print_caption()
    while not menu.time_to_quit:
        menu.print()
        menu.key_processing()
    terminal.clear()
