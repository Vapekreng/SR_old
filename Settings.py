#Меню настроек игры

from bearlibterminal import terminal
import config

# TODO: переделать меню - меню состоит из строк, каждая строка имеет имя и вызываемую функцию, а не все в кучу и ифами
# TODO: каждая строка это класс, а функция переопределяется


used_comands = [config.comand['Arrow Right'], config.comand['Arrow Left'], config.comand['Arrow Down'],
                config.comand['Arrow Up'], config.comand['right'], config.comand['left'], config.comand['down'],
                config.comand['up'], config.comand['Esc'], config.comand['Enter'], config.comand['Close']]


upper_border = 1
bottom_border = config.screen_height - 3
bgcolor = config.menu_bgcolor
lighted_bgcolor = config.menu_lighted_bgcolor
column_width = config.screen_width//2
#TODO Add spaces in print_text(), not in upper_menu_text
#TODO add auto_pick up menu
#TODO перенести текст в файл локализации
upper_menu_text = ['Управление', 'Основные']
keyset_left_text = ['Налево', 'Направо', 'Вверх', 'Вниз']
general_left_text = ['Размер шрифта', 'Язык']




# TODO подсказки и текст меню вынести в локализацию
# TODO BackSpace processing while changing keys


def get_keyset_text():
    keyset_right_text = []
    keyset_left_comands = []
    for i in range(len(config.changeble_comands)):
        name = config.changeble_comands[i]
        code = config.comand[name]
        key = config.convert_code_to_key(code)
        keyset_right_text.append(key)
        keyset_left_comands.append(name)
    return keyset_left_comands, keyset_right_text


def get_general_text():
    general_right_text = []
    general_left_comands = []
    for i in range(len(config.general_settings)):
        name = config.general_settings[i]
        value = config.settings[name]
        general_right_text.append(value)
        general_left_comands.append(name)
    return general_left_comands, general_right_text


def set_used_comands(used_comands, old_code, new_code):
    i=used_comands.index(old_code)
    used_comands[i] = new_code


# TODO Убрать used_comands и поставить проверку по config.comand.values()
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

    def print_string(self, brighness = bgcolor):
        terminal.bkcolor(brighness)
        x = self.position_of_name[self.state]
        y = 0
        text = self.text[self.state]
        terminal.printf(x, y, text)
        terminal.bkcolor(bgcolor)
        terminal.refresh()


    def go_to(self, direction):
        self.print_string()
        dif = 1
        if direction == 'prev':
            dif = -1
        self.state = (self.state + dif) % self.menu_len
        self.print_string(lighted_bgcolor)
        terminal.refresh()


    def view(self):
        n= self.state
        for i in range(self.menu_len):
            self.state = i
            self.print_string()
        self.state = n
        self.print_string(lighted_bgcolor)
        self.print_hint()
        terminal.refresh()


    def print_hint(self):
        text = self.hint
        n = len(text)
        count_of_left_spases = (config.screen_width - n)//2
        count_of_right_spases = config.screen_width - n - count_of_left_spases
        text = ' ' * count_of_left_spases + text + ' ' * count_of_right_spases
        x = 0
        y = bottom_border + 1
        terminal.printf(x, y, text)
        terminal.refresh()


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
            terminal.printf(0, y, ' '*config.screen_width)
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
        old_code = config.comand[name.strip()]
        new_code = terminal.read()
        key = config.convert_code_to_key(new_code)
        text = config.set_comand(config.comand, name, key)
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
                if key_pressed == config.comand['Esc']:
                    self.print_string()
                    break
                elif key_pressed == config.comand['Enter']:
                    if size.isdigit():
                        config.set_font_size(size)
                        font_name = config.settings['font_name']
                        font_size = int(config.settings['font_size'])
                        self.right_text[self.state] = size
                        terminal.set('font: %s, size=%d;' % (font_name, font_size))
                        terminal.refresh()
                        break
                else:
                    new_digit = config.convert_code_to_key(key_pressed)
                    if new_digit.isdigit():
                        size = size + new_digit
                        self.print_hint(size)
                key_pressed = terminal.read()


def run_menu():
    terminal.clear()
    # Separate screen for menu
    terminal.printf(0, upper_border, '-' * config.screen_width)
    terminal.printf(0, bottom_border, '-' * config.screen_width)
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
        if key_pressed == config.comand['Esc'] or key_pressed == config.comand['Close']:
            break
        if key_pressed == config.comand['left'] or key_pressed == config.comand['Arrow Left']:
            upper_menu.go_to('prev')
            current_menu = v_menues[upper_menu.state]
            current_menu.view()
        if key_pressed == config.comand['right'] or key_pressed == config.comand['Arrow Right']:
            upper_menu.go_to('next')
            current_menu = v_menues[upper_menu.state]
            current_menu.view()
        if key_pressed == config.comand['down'] or key_pressed == config.comand['Arrow Down']:
            current_menu.go_to('next')
        if key_pressed == config.comand['up'] or key_pressed == config.comand['Arrow Up']:
            current_menu.go_to('prev')
        if key_pressed == config.comand['Enter'] or key_pressed == config.comand['Space']:
            current_menu.make()
            if current_menu == general_menu and current_menu.state == 0:
                upper_menu.view()
                current_menu.view()
        key_pressed = terminal.read()


