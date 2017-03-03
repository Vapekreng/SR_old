from bearlibterminal import terminal
from config import settings, comand, screen_width, screen_height, menu_width, menu_lighted_bgcolor as lighted_bgcolor,\
    menu_bgcolor as bgcolor
import Game, Settings

# TODO: Кривое отображение меню после выхода из настроек (поправил, но лучше порефакторить)
used_comands = [comand['Esc'], comand['Enter'], comand['Close'], comand['Arrow Up'], comand['Arrow Down'],
                comand['down'], comand['up']]

class Menu:
    def __init__(self):
        self.text = ['Начать игру', 'Настройки', 'Выход']
        self.menu_len=len(self.text)
        self.menu_h = screen_height // 2 +3
        self.state=0
        self.spases = ' '*((screen_width-menu_width)//2)

    def normalize_text(self):
        for i in range(len(self.text)):
            string_name=self.text[i]
            string_name_len=len(string_name)
            left_spaces_count=(menu_width-string_name_len)//2
            right_spaces_count = menu_width - string_name_len - left_spaces_count
            self.text[i] = ' '*left_spaces_count+string_name +' '*right_spaces_count

    def print_string(self, color):
        terminal.bkcolor(bgcolor)
        terminal.printf(1, self.menu_h+self.state, self.spases)
        terminal.bkcolor(color)
        terminal.printf(1+len(self.spases), self.menu_h + self.state, self.text[self.state])
        terminal.bkcolor(bgcolor)
        terminal.refresh()

    def view(self):
        terminal.bkcolor(bgcolor)
        terminal.clear()
        self.state=0
        self.print_string(lighted_bgcolor)
        for i in range(1,self.menu_len):
            self.state=i
            self.print_string(bgcolor)
        self.state=0
        terminal.refresh()

    def up(self):
        self.print_string(bgcolor)
        self.state = (self.state - 1) % self.menu_len
        self.print_string(lighted_bgcolor)

    def down(self):
        self.print_string(bgcolor)
        self.state = (self.state + 1) % self.menu_len
        self.print_string(lighted_bgcolor)

def run_main_menu():
    main_menu=Menu()
    main_menu.normalize_text()
    main_menu.view()
    key_pressed=terminal.read()
    while True:
        while key_pressed not in used_comands:
            key_pressed = terminal.read()
        if key_pressed == comand['Enter']:
            if main_menu.state == 0:
                Game.run_game()
                main_menu.view()
            elif main_menu.state == 1:
                Settings.run_menu()
                main_menu.view()
            elif main_menu.state == 2:
                key_pressed=comand['Esc']
        if key_pressed == comand['Esc'] or key_pressed == comand['Close']:
            break
        if key_pressed == comand['up'] or key_pressed == comand['Arrow Up']:
            main_menu.up()
        if key_pressed == comand['down'] or key_pressed == comand['Arrow Down']:
            main_menu.down()
        key_pressed = terminal.read()

terminal.open()
terminal.set('font: %s, size=%d;' % (settings['font_name'], int(settings['font_size'])))
run_main_menu()
