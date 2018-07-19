from bearlibterminal import terminal

import localization
import keyset
import adventure
import menu_controls
import config
import menu_settings

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
        self.code_to_comand_dict = keyset.current_keyset.get_code_to_comand_dict()
        self.comand_to_code_dict = keyset.current_keyset.get_comands_to_code()
        self.button_names = MAIN_MENU_NAMES
        self.length = len(self.button_names)
        self._set_translated_button_names()
        self.position = 0
        self.width = self._init_menu_width()
        self.init_coord_x = self._init_init_coord_x()
        self.init_coord_y = self._get_init_coord_y()
        self.comand_to_action_dict = {}
        self._set_comand_to_action_dict()
        self.button_to_action_dict = {}
        self._set_button_to_action_dict()
        self.used_codes = []
        self._set_used_codes()

    def _set_button_to_action_dict(self):
        self.button_to_action_dict[0] = adventure.new_game
        self.button_to_action_dict[1] = adventure.load_game
        self.button_to_action_dict[2] = menu_controls.main_loop
        self.button_to_action_dict[3] = menu_settings.main_loop
        self.button_to_action_dict[4] = self._set_quit

    def _set_comand_to_action_dict(self):
        self.comand_to_action_dict['up'] = self._prev_button
        self.comand_to_action_dict['arrow up'] = self._prev_button
        self.comand_to_action_dict['down'] = self._next_button
        self.comand_to_action_dict['arrow down'] = self._next_button
        self.comand_to_action_dict['enter'] = self._press_button
        self.comand_to_action_dict['esc'] = self._set_quit
        self.comand_to_action_dict['close'] = self._set_quit

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

    def _set_used_codes(self):
        for comand in MAIN_MENU_USED_COMANDS:
            code = self.comand_to_code_dict[comand]
            self.used_codes.append(code)

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
        code = self._get_code()
        comand = self.code_to_comand_dict[code]
        self.comand_to_action_dict[comand]()

    def _get_code(self):
        code = terminal.read()
        while code not in self.used_codes:
            code = terminal.read()
        while terminal.has_input():
            terminal.read()
        return code

    def _set_position(self, new_position):
        self.position = new_position

    def _set_quit(self):
        self.time_to_quit = True

    def _press_button(self):
        self.button_to_action_dict[self.position]()

    def _next_button(self):
        new_position = (self.position + 1) % self.length
        self._set_position(new_position)

    def _prev_button(self):
        new_position = (self.position - 1) % self.length
        self._set_position(new_position)

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
