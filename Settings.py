from bearlibterminal import terminal
import config
#Меню настроек игры


used_comands = [config.comand['Arrow Right'], config.comand['Arrow Left'], config.comand['Arrow Down'],
                config.comand['Arrow Up'], config.comand['right'], config.comand['left'], config.comand['down'],
                config.comand['up'], config.comand['Esc'], config.comand['Enter'], config.comand['Close']]


upper_border = 2
bottom_border = config.screen_height - 3
bgcolor = config.menu_bgcolor
lighted_bgcolor = config.menu_lighted_bgcolor


def set_used_comands(used_comands, old_code, new_code):
    i=used_comands.index(old_code)
    used_comands[i] = new_code


# TODO Собрать меню в классы: класс меню - классы верт и гор меню, добавить атрибут подсказки и выводить его снизу
# TODO экрана. Поменять атрибут name на normalize_name и сделать вывод на русском. Атрибут name - туда закинуть
# TODO оригинальные названия команд. Убрать used_comands и поставить проверку по config.comand.values()



# Имена меню с пробелами до и после названия
class Upper_menu:
    def __init__(self):
        self.menu_name = [' Основные ', ' Управление ', ' Автоподбор ', ' Меню 4 ', ' Меню 5', ' Меню 6 ']
        self.menu_len = len(self.menu_name)
        self.name_position=[]
        position=0
        for name in self.menu_name:
            self.name_position.append(position)
            position += len(name)
        self.state = 0


    def print_position(self, brighness):
        terminal.bkcolor(brighness)
        terminal.printf(self.name_position[self.state], 0, self.menu_name[self.state])
        terminal.bkcolor(bgcolor)
        terminal.refresh()


    def move_right(self):
        self.print_position(bgcolor)
        self.state = (self.state + 1) % self.menu_len
        self.print_position(lighted_bgcolor)


    def move_left(self):
        self.print_position(bgcolor)
        self.state = (self.state -1) % self.menu_len
        self.print_position(lighted_bgcolor)


    def view(self):
        self.print_position(lighted_bgcolor)
        for i in range(1, self.menu_len):
            self.state = i
            self.print_position(bgcolor)
        self.state = 0
        terminal.printf(0, upper_border - 1, '-' * config.screen_width)
        terminal.printf(0, bottom_border +1, '-' * config.screen_width)
        terminal.refresh()

class Keyset_menu:
    def __init__(self):
        self.names_width = config.screen_width//2
        self.name = []
        self.bottom_border = config.screen_height - 2
        for name in config.changeble_comands:
            self.name.append(name + ' ' * (self.names_width - len(name)))
        self.key = []
        for name in self.name:
            code = config.comand[name.strip()]
            key = config.convert_code_to_key(code)
            self.key.append(key)
        self.menu_len = len(self.name)
        self.state = 0

    def print_position(self, brighness):
        terminal.bkcolor(brighness)
        x = 0
        y = upper_border + self.state
        text = self.name[self.state]
        terminal.printf(x, y, text)
        terminal.bkcolor(bgcolor)
        x = self.names_width +1
        text = self.key[self.state] + ' ' * (config.screen_width - x)
        terminal.printf(x, y, text )
        terminal.refresh()


    def view(self):
        self.print_position(lighted_bgcolor)
        for i in range(1, self.menu_len):
            self.state = i
            self.print_position(bgcolor)
        self.state = 0
        terminal.refresh()

    def move_up(self):
        self.print_position(bgcolor)
        self.state = (self.state -1) % self.menu_len
        self.print_position(lighted_bgcolor)
        terminal.refresh()


    def move_down(self):
        self.print_position(bgcolor)
        self.state = (self.state + 1) % self.menu_len
        self.print_position(lighted_bgcolor)
        terminal.refresh()


    def set_value(self):
        x = self.names_width +1
        y = upper_border + self.state
        text = 'Нажмите клавишу или Esc для отмены'
        terminal.printf(x, y, text + ' ' * (config.screen_width - self.names_width - len(text)))
        terminal.refresh()
        name = self.name[self.state]
        old_code = config.comand[name.strip()]
        new_code = terminal.read()
        key = config.convert_code_to_key(new_code)
        name = self.name[self.state]
        text = config.set_comand(config.comand, self.name[self.state], key)
        if text == key:
            self.key[self.state] = key
            set_used_comands(used_comands, old_code, new_code)
        terminal.printf(x, y, text + ' ' * (config.screen_width - self.names_width - len(text)))
        terminal.refresh()


def run_menu():
    terminal.clear()
    upper_menu = Upper_menu()
    upper_menu.view()
    h_menu = Keyset_menu()
    h_menu.view()
    key_pressed = terminal.read()
    while True:
        while key_pressed not in used_comands:
            key_pressed = terminal.read()
            terminal.clear()
        if key_pressed == config.comand['Esc'] or key_pressed == config.comand['Close']:
            break
        if key_pressed == config.comand['left'] or key_pressed == config.comand['Arrow Left']:
            upper_menu.move_left()
        if key_pressed == config.comand['right'] or key_pressed == config.comand['Arrow Right']:
            upper_menu.move_right()
        if key_pressed == config.comand['down'] or key_pressed == config.comand['Arrow Down']:
            h_menu.move_down()
        if key_pressed == config.comand['up'] or key_pressed == config.comand['Arrow Up']:
            h_menu.move_up()
        if key_pressed == config.comand['Enter']:
            h_menu.set_value()
        key_pressed = terminal.read()