from bearlibterminal import terminal
import config
#Меню настроек игры


used_comands = [config.comand['Arrow Right'], config.comand['Arrow Left'], config.comand['Arrow Down'],
                config.comand['Arrow Up'], config.comand['right'], config.comand['left'], config.comand['down'],
                config.comand['up'], config.comand['Esc'], config.comand['Enter'], config.comand['Close']]


upper_border = 1
bottom_border = config.screen_height - 3
bgcolor = config.menu_bgcolor
lighted_bgcolor = config.menu_lighted_bgcolor
column_width = config.screen_width//2
#TODO Add spaces in print_text(), not in upper_menu_text
upper_menu_text = [' Управление ', ' Основные ', ' Автоподбор ', ' Меню 4 ', ' Меню 5', ' Меню 6 ']
keyset_left_text = ['Налево', 'Направо', 'Вверх', 'Вниз']




#TODO подсказки и текст меню вынести в локализацию


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


def set_used_comands(used_comands, old_code, new_code):
    i=used_comands.index(old_code)
    used_comands[i] = new_code


# TODO Убрать used_comands и поставить проверку по config.comand.values()
# TODO Добавить трибут глобал хинт для вывода внизу экрана


class Horizontal_menu():


    def __init__(self, text):
        self.text = text
        self.menu_len = len(self.text)
        self.state = 0
        self.position_of_name = []
        self.hint = 'Enter или Spase для изменения, Esc - выход'
        position = 0
        for name in self.text:
            self.position_of_name.append(position)
            position += len(name)

    def print_string(self, brighness):
        terminal.bkcolor(brighness)
        x = self.position_of_name[self.state]
        y = 0
        text = self.text[self.state]
        terminal.printf(x, y, text)
        terminal.bkcolor(bgcolor)
        terminal.refresh()


    def go_to(self, direction):
        self.print_string(bgcolor)
        dif = 1
        if direction == 'prev':
            dif = -1
        self.state = (self.state + dif) % self.menu_len
        self.print_string(lighted_bgcolor)
        terminal.refresh()


    def view(self):
        self.print_string(lighted_bgcolor)
        for i in range(1, self.menu_len):
            self.state = i
            self.print_string(bgcolor)
        self.state = 0
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
        self.print_string(bgcolor)
        self.print_string(bgcolor, 'right')
        dif = 1
        if direction == 'prev':
            dif = -1
        self.state = (self.state + dif) % self.menu_len
        self.print_string(lighted_bgcolor)
        terminal.refresh()


    def view(self):
        self.print_string(lighted_bgcolor)
        self.print_string(bgcolor, 'right')
        for i in range(1, self.menu_len):
            self.state = i
            self.print_string(bgcolor)
            self.print_string(bgcolor, 'right')
        self.state = 0
        terminal.refresh()


    def print_string(self, brighness, column='left'):
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
        text = hint + ' ' * (column_width - len(hint))
        x = column_width +1
        y = upper_border +1 + self.state
        terminal.printf(x, y, text)
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
        self.print_hint(text)
        terminal.refresh()


class Video_menu(Vertical_menu):


    def make(self):
        pass



def run_menu():
    terminal.clear()
    # Separate screen for menu
    terminal.printf(0, upper_border, '-' * config.screen_width)
    terminal.printf(0, bottom_border, '-' * config.screen_width)
    # Initialise upper menu
    #TODO перенести текст в файл локализации
    upper_menu = Horizontal_menu(upper_menu_text)
    upper_menu.view()
    # Initialise keyset menu
    #TODO перенести текст в файл локализации
    keyset_left_comands, keyset_right_text = get_keyset_text()
    keyset_menu = Keyset_menu(keyset_left_text, keyset_right_text, keyset_left_comands)
    keyset_menu.view()
    current_menu = keyset_menu
    key_pressed = terminal.read()
    while True:
        while key_pressed not in used_comands:
            key_pressed = terminal.read()
            terminal.clear()
        if key_pressed == config.comand['Esc'] or key_pressed == config.comand['Close']:
            break
        if key_pressed == config.comand['left'] or key_pressed == config.comand['Arrow Left']:
            upper_menu.go_to('prev')
        if key_pressed == config.comand['right'] or key_pressed == config.comand['Arrow Right']:
            upper_menu.go_to('next')
        if key_pressed == config.comand['down'] or key_pressed == config.comand['Arrow Down']:
            current_menu.go_to('next')
        if key_pressed == config.comand['up'] or key_pressed == config.comand['Arrow Up']:
            current_menu.go_to('prev')
        if key_pressed == config.comand['Enter'] or key_pressed == config.comand['Space']:
            current_menu.make()
        key_pressed = terminal.read()


