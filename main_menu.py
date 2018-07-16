from bearlibterminal import terminal

import localization
import keyset
import adventure
import controls
import config
import game_settings

MAIN_MENU_NAMES = ['New game', 'Load game', 'Controls', 'Settings', 'Exit']
MAIN_MENU_USED_COMANDS = ['up', 'down', 'arrow up', 'arrow down', 'enter', 'esc', 'close']
SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT
COUNT_OF_SPACES = 2
COUNT_OF_EMPTY_BOTTOM_LINES = 5
BG_COLOR_LIGHTED = 'dark grey'
BG_COLOR_NORMAL = 'black'


class MainMenu:

    def __init__(self):
        self.time_to_quit = False
        self.keyset = keyset.current_keyset.get_codes()
        self.button_names = MAIN_MENU_NAMES
        self.length = len(self.button_names)
        self._set_translated_button_names()
        self.position = 0
        self.width = self._init_menu_width()
        self.init_coord_x = self._init_init_coord_x()
        self.init_coord_y = self._get_init_coord_y()
        self.key_comands = {}
        self._init_dict_of_key_comands()
        self.button_comands = {}
        self._init_dict_of_button_comands()

    def _init_dict_of_button_comands(self):
        self.button_comands[0] = adventure.new_game
        self.button_comands[1] = adventure.load_game
        self.button_comands[2] = controls.main_loop
        self.button_comands[3] = game_settings.main_loop
        self.button_comands[3] = self._set_quit

    def _init_dict_of_key_comands(self):
        self.key_comands['up'] = self._prev_button
        self.key_comands['arrow up'] = self._prev_button
        self.key_comands['down'] = self._next_button
        self.key_comands['arrow down'] = self._next_button
        self.key_comands['enter'] = self._press_button
        self.key_comands['esc'] = self._set_quit
        self.key_comands['close'] = self._set_quit

    def _init_menu_width(self):
        max_len = len(max(self.button_names))
        max_len = max_len + max_len % 2 + COUNT_OF_SPACES * 2
        return max_len

    def _init_init_coord_x(self):
        coord_x = (SCREEN_WIDTH - self.width) // 2
        return coord_x

    def _get_init_coord_y(self):
        coord_y = SCREEN_HEIGHT - COUNT_OF_EMPTY_BOTTOM_LINES - self.length
        return coord_y

    def print(self):
        length = self.length
        for position in range(length):
            self._print_button(position)
        terminal.refresh()

    def _print_button(self, position):
        init_text = self.button_names[position]
        normilized_text = init_text.center(self.width)
        x = self.init_coord_x
        y = self.init_coord_y + position
        if self.position == position:
            terminal.bkcolor(BG_COLOR_LIGHTED)
        terminal.printf(x, y, normilized_text)
        terminal.bkcolor(BG_COLOR_NORMAL)

    def key_processing(self):
        key = self._get_code()
        comand = self.keyset[key]
        self.key_comands[comand]()

    def _get_code(self):
        code = terminal.read()
        comand = self._convert_code_to_comand(code)
        while comand not in MAIN_MENU_USED_COMANDS:
            code = terminal.read()
            comand = self._convert_code_to_comand(code)
        while terminal.has_input():
            terminal.read()
        return code

    def _set_position(self, new_position):
        self.position = new_position

    def _set_quit(self):
        self.time_to_quit = True

    def _press_button(self):
        self.button_comands[self.position]()

    def _next_button(self):
        new_position = (self.position + 1) % self.length
        self._set_position(new_position)

    def _prev_button(self):
        new_position = (self.position - 1) % self.length
        self._set_position(new_position)

    def _convert_code_to_comand(self, code):
        comand = ''
        try:
            comand = self.keyset[code]
        except KeyError:
            pass
        return comand

    def _set_translated_button_names(self):
        for i in range(self.length):
            text = self.button_names[i]
            self.button_names[i] = localization.current_localization.translate(text)


def main_loop():
    main_menu = MainMenu()
    while not main_menu.time_to_quit:
        main_menu.print()
        main_menu.key_processing()

# TODO После захода в меню настроек и смены языка, скорее всего, тут  останется старый язык. Сделать передачу сообщения
# TODO от main_menu.key_processing с помощью return
