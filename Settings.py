import Config
from bearlibterminal import terminal

upper_border = 1
bottom_border = Config.screen_height - 3
bgcolor = Config.menu_bgcolor
lighted_bgcolor = Config.menu_lighted_bgcolor
column_width = Config.screen_width//2
# TODO add auto_pick up menu
# TODO BackSpace processing while changing keys


def set_used_comands(used_comands, old_code, new_code):
    i=used_comands.index(old_code)
    used_comands[i] = new_code


# TODO Добавить трибут глобал хинт для вывода внизу экрана


class Horizontal_menu():


    def __init__(self, text):
        self.text = text
        self.menu_len = len(self.text)
        for i in range(self.menu_len):
            self.text[i] = ' ' + self.text[i] + ' '
        self.state = 0
        self.position_of_name = []
        self.hint = 'Enter или Spase для изменения, Esc - выход'
        position = 0
        for name in self.text:
            self.position_of_name.append(position)
            position += len(name)




# Имена меню с пробелами до и после названия
#TODO добавить метод добавления пробелов к строке
class Vertical_menu:
    def __init__(self, left_text, right_text, left_comands):
        self.left_text = left_text
        self.left_comands = left_comands
        self.right_text = right_text
        self.menu_len = len(self.left_text)
        self.state = 0
        for i in range(self.menu_len):
            self.left_text[i] = left_text[i] + ' ' * (column_width - len(left_text[i]))
            self.right_text[i] = right_text[i] + ' ' * (column_width - len(right_text[i]))


    def go_to(self, direction):
        self.print_string()
        self.print_string(column = 'right')
        dif = 1
        if direction == 'prev':
            dif = -1
        self.state = (self.state + dif) % self.menu_len
        self.print_string(lighted_bgcolor)
        terminal.refresh()


    def view(self):
        n= self.state
        for y in range(upper_border+1, bottom_border):
            terminal.printf(0, y, ' '*Config.screen_width)
        for i in range(self.menu_len):
            self.state = i
            self.print_string()
            self.print_string(column = 'right')
        self.state = n
        self.print_string(lighted_bgcolor)
        self.print_string(column = 'right')
        terminal.refresh()


    def print_string(self, brighness = bgcolor, column='left'):
        terminal.bkcolor(brighness)
        column = column.lower()
        if column == 'left':
            x = 0
            text = self.left_text[self.state]
        elif column == 'right':
            x = column_width + 1
            text = self.right_text[self.state]
        y = upper_border + 1 + self.state
        terminal.printf(x, y, text)
        terminal.bkcolor(bgcolor)
        terminal.refresh()


    def print_hint(self, hint):
        hint = hint + ' ' * (column_width - len(hint))
        x = column_width +1
        y = upper_border +1 + self.state
        terminal.printf(x, y, hint)
        terminal.refresh()


# TODO Добавить метод смены управления
class Keyset_menu(Vertical_menu):


    def make(self):
        self.print_hint('Нажмите клавишу или Esc для отмены')
        name = self.left_comands[self.state]
        old_code = Config.comand[name.strip()]
        new_code = terminal.read()
        key = Config.convert_code_to_key(new_code)
        text = Config.set_comand(Config.comand, name, key)
        if text == key:
            set_used_comands(used_comands, old_code, new_code)
            text = text + ' ' * (column_width - len(text))
            self.right_text[self.state] = text
        else:
            text = text + ' ' * (column_width - len(text))
        self.print_hint(text)
        terminal.refresh()


class General_menu(Vertical_menu):


    def make(self):
        if self.state == 0:
            self.print_hint('Введите размер шрифта')
            key_pressed = terminal.read()
            size = ''
            while True:
                if key_pressed == Config.comand['Esc']:
                    self.print_string()
                    break
                elif key_pressed == Config.comand['Enter']:
                    if size.isdigit():
                        Config.set_font_size(size)
                        font_name = Config.settings['font_name']
                        font_size = int(Config.settings['font_size'])
                        self.right_text[self.state] = size
                        terminal.set('font: %s, size=%d;' % (font_name, font_size))
                        terminal.refresh()
                        break
                else:
                    new_digit = Config.convert_code_to_key(key_pressed)
                    if new_digit.isdigit():
                        size = size + new_digit
                        self.print_hint(size)
                key_pressed = terminal.read()


def run_menu():
    terminal.clear()
    # Separate screen for menu
    terminal.printf(0, upper_border, '-' * Config.screen_width)
    terminal.printf(0, bottom_border, '-' * Config.screen_width)
    # Initialise menues
    upper_menu = Horizontal_menu(upper_menu_text)
    upper_menu.view()
    keyset_left_comands, keyset_right_text = get_keyset_text()
    keyset_menu = Keyset_menu(keyset_left_text, keyset_right_text, keyset_left_comands)
    keyset_menu.view()
    genera_left_commands, general_right_text = get_general_text()
    general_menu = General_menu(general_left_text, general_right_text, genera_left_commands)
    v_menues = [keyset_menu, general_menu]
    current_menu = v_menues[upper_menu.state]
    key_pressed = terminal.read()
    while True:
        while key_pressed not in used_comands:
            key_pressed = terminal.read()
        if key_pressed == Config.comand['Esc'] or key_pressed == Config.comand['Close']:
            break
        if key_pressed == Config.comand['left'] or key_pressed == Config.comand['Arrow Left']:
            upper_menu.go_to('prev')
            current_menu = v_menues[upper_menu.state]
            current_menu.view()
        if key_pressed == Config.comand['right'] or key_pressed == Config.comand['Arrow Right']:
            upper_menu.go_to('next')
            current_menu = v_menues[upper_menu.state]
            current_menu.view()
        if key_pressed == Config.comand['down'] or key_pressed == Config.comand['Arrow Down']:
            current_menu.go_to('next')
        if key_pressed == Config.comand['up'] or key_pressed == Config.comand['Arrow Up']:
            current_menu.go_to('prev')
        if key_pressed == Config.comand['Enter'] or key_pressed == Config.comand['Space']:
            current_menu.make()
            if current_menu == general_menu and current_menu.state == 0:
                upper_menu.view()
                current_menu.view()
        key_pressed = terminal.read()


