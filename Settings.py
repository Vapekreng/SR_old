from bearlibterminal import terminal
from config import screen_width, screen_height, menu_bgcolor, menu_lighted_bgcolor, comand


used_comands = [comand['Arrow Right'], comand['Arrow Left'], comand['right'], comand['left'], comand['Esc'],
                comand['Enter'], comand['Close']]


class menu:
    def __init__(self):
        self.menu_name = [' Основные ', ' Управление ', ' Меню 3 ', ' Меню 4 ', ' Меню 5', ' Меню 6 ']
        self.menu_len = len(self.menu_name)
        self.name_position=[]
        position=0
        for name in self.menu_name:
            self.name_position.append(position)
            position += len(name)
        self.state = 0
        self.bgcolor = menu_bgcolor
        self.lighted_bgcolor = menu_lighted_bgcolor


    def print_position(self,bgcolor):
        terminal.bkcolor(bgcolor)
        terminal.printf(self.name_position[self.state], 1, self.menu_name[self.state])
        terminal.refresh()


    def move_right(self):
        self.print_position(self.bgcolor)
        self.state = (self.state + 1) % self.menu_len
        self.print_position(self.lighted_bgcolor)


    def move_left(self):
        self.print_position(self.bgcolor)
        self.state = (self.state -1) % self.menu_len
        self.print_position(self.lighted_bgcolor)


    def view(self):
        self.print_position(self.lighted_bgcolor)
        for i in range(1, self.menu_len):
            self.state = i
            self.print_position(self.bgcolor)
        self.state = 0


def run_menu():
    terminal.clear()
    upper_menu = menu()
    upper_menu.view()
    key_pressed = terminal.read()
    while True:
        while key_pressed not in used_comands:
            key_pressed = terminal.read()
        if key_pressed == comand['Esc'] or key_pressed == comand['Close']:
            break
        if key_pressed == comand['left'] or key_pressed == comand['Arrow Left']:
            upper_menu.move_left()
        if key_pressed == comand['right'] or key_pressed == comand['Arrow Right']:
            upper_menu.move_right()
        key_pressed = terminal.read()
