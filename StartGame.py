from bearlibterminal import terminal
import config, Game, Settings


bgcolor = config.menu_bgcolor
lighted_bgcolor = config.menu_lighted_bgcolor


#Выводит на экран главное меню игры и передает управление дальше по пунктам
class Menu:
    def __init__(self):
        self.text = ['Начать игру', 'Настройки', 'Выход']
        self.menu_len=len(self.text)
        self.menu_h = config.screen_height // 2 +3
        self.state=0
        self.spases = ' '*((config.screen_width-config.menu_width)//2)

    def normalize_text(self):
        for i in range(len(self.text)):
            string_name=self.text[i]
            string_name_len=len(string_name)
            left_spaces_count=(config.menu_width-string_name_len)//2
            right_spaces_count = config.menu_width - string_name_len - left_spaces_count
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
        while key_pressed not in config.comand.values():
            key_pressed = terminal.read()
            terminal.clear()
        if key_pressed == config.comand['Enter']:
            if main_menu.state == 0:
                Game.run_game()
                main_menu.view()
            elif main_menu.state == 1:
                Settings.run_menu()
                main_menu.view()
            elif main_menu.state == 2:
                key_pressed = config.comand['Esc']
        if key_pressed == config.comand['Esc'] or key_pressed == config.comand['Close']:
            break
        if key_pressed == config.comand['up'] or key_pressed == config.comand['Arrow Up']:
            main_menu.up()
        if key_pressed == config.comand['down'] or key_pressed == config.comand['Arrow Down']:
            main_menu.down()
        key_pressed = terminal.read()

terminal.open()
terminal.set('font: %s, size=%d;' % (config.settings['font_name'], int(config.settings['font_size'])))
run_main_menu()
