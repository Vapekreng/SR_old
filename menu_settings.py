import os.path

from bearlibterminal import terminal

import keyset
import config
import localization
import settings

_SETTINGS_MENU_USED_COMANS = ['up', 'down', 'left', 'right', 'arrow up', 'arrow down', 'arrow left', 'arrow right',
                              'esc']
_SETTINGS_MENU_BUTTONS_NAMES = ['language', 'font size']
_SCREEN_WIDTH = config.SCREEN_WIDTH
_SCREEN_HEIGHT = config.SCREEN_HEIGHT
_TERMINAL_COLOR_NORMAL = 'white'
_TERMINAL_COLOR_LIGHTED = 'yellow'
_CAPTION_START_POSITION = [0, 1]
_CAPTION_BORDER_POSITION = [0, 2]
_CAPTION_NAME = 'Game settings'
_BORDER_SYMBOL = '-'
_LEFT_COLUMN_START_POSITION = [10, 4]
_RIGHT_COLUMN_START_POSITION = [_SCREEN_WIDTH // 2 + 1, 4]
_RIGHT_COLUMN_WIDTH = _SCREEN_WIDTH // 2
_LEFT_BRACKETS = '<<< '
_RIGHT_BRACKETS = ' >>>'
_LOCALIZATION_PATH = 'DATA\\localization'

class MenuSettings:

    def __init__(self):
        self.position = 0
        self.buttons = []
        self._set_buttons()
        self.code_to_comand_dict = keyset.current_keyset.get_code_to_comand_dict()
        self.comand_to_code_dict = keyset.current_keyset.get_comands_to_code_dict()
        self.comand_to_action_dict = {}
        self.languages = self._get_languages()
        self._next_value_list = []
        self._set_next_value_list()
        self._prev_value_list = []
        self._set_prev_value_list()
        self._set_comand_to_action_dict()
        self.used_codes = []
        self._set_used_codes()
        self.time_to_quit = False
        self.length = len(_SETTINGS_MENU_BUTTONS_NAMES)
        self.count_of_languages = len(self.languages)


    def _set_buttons(self):
        self.buttons = [{'name': 'language', 'value': settings.current_settings.language},
                        {'name': 'font size', 'value': settings.current_settings.font_size}]

    def _set_used_codes(self):
        self.used_codes = []
        for comand in _SETTINGS_MENU_USED_COMANS:
            code = self.comand_to_code_dict[comand]
            self.used_codes.append(code)

    def _set_comand_to_action_dict(self):
        self.comand_to_action_dict['up'] = self._prev_button
        self.comand_to_action_dict['arrow up'] = self._prev_button
        self.comand_to_action_dict['down'] = self._next_button
        self.comand_to_action_dict['arrow down'] = self._next_button
        self.comand_to_action_dict['left'] = self._prev_value
        self.comand_to_action_dict['arrow left'] = self._prev_value
        self.comand_to_action_dict['right'] = self._next_value
        self.comand_to_action_dict['arrow right'] = self._next_value
        self.comand_to_action_dict['esc'] = self._set_quit

    def _set_next_value_list(self):
        self._next_value_list = [self._next_language, self._next_font_size]

    def _set_prev_value_list(self):
        self._prev_value_list = [self._prev_language, self._prev_font_size]

    def _prev_value(self):
        self._prev_value_list[self.position]()

    def _next_value(self):
        self._next_value_list[self.position]()

    def _next_language(self):
        current_language = settings.current_settings.language
        current_language_index = self.languages.index(current_language)
        new_language_index = (current_language_index + 1) % self.count_of_languages
        new_language = self.languages[new_language_index]
        self._set_language(new_language)

    def _prev_language(self):
        current_language = settings.current_settings.language
        current_language_index = self.languages.index(current_language)
        new_language_index = (current_language_index - 1) % self.count_of_languages
        new_language = self.languages[new_language_index]
        self._set_language(new_language)

    def _next_font_size(self):
        current_font_size = settings.current_settings.font_size
        new_font_size = current_font_size + 1
        settings.current_settings.set_font_size(new_font_size)
        self._set_buttons()
        self.print_caption()
        self.print()

    def _prev_font_size(self):
        current_font_size = settings.current_settings.font_size
        new_font_size = current_font_size - 1
        settings.current_settings.set_font_size(new_font_size)
        self._set_buttons()
        self.print_caption()
        self.print()

    def _set_language(self, new_language):
        settings.current_settings.set_language(new_language)
        localization.current_localization.update_localization(new_language)
        self._set_buttons()
        self.print_caption()
        self.print()

    @staticmethod
    def _get_languages():
        languages = []
        localization_files_names = os.listdir(path=_LOCALIZATION_PATH)
        for file_name in localization_files_names:
            new_language_start_index = file_name.index('-') + 1
            new_language_last_index = file_name.index('.')
            new_language = file_name[new_language_start_index: new_language_last_index]
            languages.append(new_language)
        return languages

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
        while code not in self.used_codes:
            code = terminal.read()
        while terminal.has_input():
            terminal.read()
        return code

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
        terminal.printf(x, y, ' ' * _SCREEN_WIDTH)
        text = self.buttons[index]['name']
        localized_text = localization.current_localization.translate(text)
        terminal.printf(x, y, localized_text)

    def _print_right_part(self, index):
        x0, y0 = _RIGHT_COLUMN_START_POSITION
        x = x0
        y = y0 + index
        text = self.buttons[index]['value']
        text = str(text)
        localized_text = localization.current_localization.translate(text)
        if self.position == index:
            localized_text = _LEFT_BRACKETS + localized_text + _RIGHT_BRACKETS
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
    menu = MenuSettings()
    menu.print_caption()
    while not menu.time_to_quit:
        menu.print()
        menu.key_processing()
    terminal.clear()
