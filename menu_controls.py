from bearlibterminal import terminal

import keyset
import config
import localization

_CONTROLS_MENU_USED_COMANS = ['up', 'down', 'arrow up', 'arrow down', 'enter', 'esc']
_CHANGEBLE_COMANDS = keyset.CHANGEBLE_COMANDS
_INVITE_TO_PRINT = '<<< ??? >>>'
_SCREEN_WIDTH = config.SCREEN_WIDTH
_SCREEN_HEIGHT = config.SCREEN_HEIGHT
_TERMINAL_COLOR_NORMAL = 'white'
_TERMINAL_COLOR_LIGHTED = 'yellow'
_CAPTION_START_POSITION = [0, 1]
_CAPTION_BORDER_POSITION = [0, 2]
_CAPTION_NAME = 'Control settings'
_BORDER_SYMBOL = '-'
_LEFT_COLUMN_START_POSITION = [10, 4]
_RIGHT_COLUMN_START_POSITION = [_SCREEN_WIDTH // 2 + 1, 4]
_RIGHT_COLUMN_WIDTH = _SCREEN_WIDTH // 2


class MenuControls:

    def __init__(self):
        self.position = 0
        self.buttons = self._get_buttons()
        self.code_to_comand_dict = keyset.current_keyset.get_code_to_comand_dict()
        self.comand_to_code_dict = keyset.current_keyset.get_comands_to_code_dict()
        self.comand_to_action_dict = {}
        self._set_comand_to_action_dict()
        self.used_codes = []
        self._set_used_codes()
        self.time_to_quit = False
        self.length = len(_CHANGEBLE_COMANDS)

    @staticmethod
    def _get_buttons():
        buttons = []
        comand_to_code_dict = keyset.current_keyset.get_comands_to_code_dict()
        for comand in _CHANGEBLE_COMANDS:
            code = comand_to_code_dict[comand]
            key = keyset.current_keyset.convert_code_to_key_func(code)
            buttons.append({'comand': comand, 'key': key})
        return buttons

    def _set_used_codes(self):
        self.used_codes = []
        for comand in _CONTROLS_MENU_USED_COMANS:
            code = self.comand_to_code_dict[comand]
            self.used_codes.append(code)

    def _set_comand_to_action_dict(self):
        self.comand_to_action_dict['up'] = self._prev_button
        self.comand_to_action_dict['arrow up'] = self._prev_button
        self.comand_to_action_dict['down'] = self._next_button
        self.comand_to_action_dict['arrow down'] = self._next_button
        self.comand_to_action_dict['enter'] = self._press_button
        self.comand_to_action_dict['esc'] = self._set_quit

    def _set_quit(self):
        self.time_to_quit = True

    def _set_position(self, new_position):
        self.position = new_position

    def _prev_button(self):
        new_position = (self.position - 1) % self.length
        self._set_position(new_position)

    def _next_button(self):
        new_position = (self.position + 1) % self.length
        self._set_position(new_position)

    def key_processing(self):
        code = self._get_code()
        comand = self.code_to_comand_dict[code]
        action = self.comand_to_action_dict[comand]
        action()

    def _get_code(self):
        code = terminal.read()
        self._set_used_codes()
        while code not in self.used_codes:
            code = terminal.read()
        while terminal.has_input():
            terminal.read()
        return code

    def _press_button(self):
        self._print_invite_to_change_key()
        new_code = terminal.read()
        new_key = keyset.current_keyset.convert_code_to_key_func(new_code)
        new_comand = self.buttons[self.position]['comand']
        keyset.current_keyset.set_comand_to_code(new_comand, new_key)
        self._get_buttons()
        self.code_to_comand_dict = keyset.current_keyset.get_code_to_comand_dict()
        self.comand_to_code_dict = keyset.current_keyset.get_comands_to_code_dict()
        self.buttons = self._get_buttons()
        keyset.current_keyset.save()

    def _print_invite_to_change_key(self):
        x, y = _RIGHT_COLUMN_START_POSITION
        y = y + self.position
        text = _INVITE_TO_PRINT.center(_SCREEN_WIDTH // 2)
        terminal.color(_TERMINAL_COLOR_LIGHTED)
        terminal.printf(x, y, text)
        terminal.color(_TERMINAL_COLOR_NORMAL)
        terminal.refresh()

    def _print_button(self, index):
        if index == self.position:
            terminal.color(_TERMINAL_COLOR_LIGHTED)
        self._print_left_part(index)
        self._print_right_part(index)
        terminal.color(_TERMINAL_COLOR_NORMAL)

    def _print_left_part(self, index):
        x0, y0 = _LEFT_COLUMN_START_POSITION
        x = x0
        y = y0 + index
        text = self.buttons[index]['comand']
        localized_text = localization.current_localization.translate(text)
        terminal.printf(x, y, localized_text)

    def _print_right_part(self, index):
        x0, y0 = _RIGHT_COLUMN_START_POSITION
        x = x0
        y = y0 + index
        text = self.buttons[index]['key']
        localized_text = localization.current_localization.translate(text)
        normalized_text = localized_text.center(_RIGHT_COLUMN_WIDTH)
        terminal.printf(x, y, normalized_text)

    def print(self):
        for i in range(self.length):
            self._print_button(i)
        terminal.refresh()

    @staticmethod
    def print_caption():
        x0, y0 = _CAPTION_START_POSITION
        text = _CAPTION_NAME
        localized_text = localization.current_localization.translate(text)
        normalized_text = localized_text.center(_SCREEN_WIDTH)
        terminal.printf(x0, y0, normalized_text)
        x0, y0 = _CAPTION_BORDER_POSITION
        border = _BORDER_SYMBOL * _SCREEN_WIDTH
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
