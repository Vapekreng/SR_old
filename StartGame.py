from bearlibterminal import terminal
import config, Game, Settings, localization

# TODO: переделать меню - меню состоит из строк, каждая строка имеет имя и вызываемую функцию, а не все в кучу и ифами
# TODO: каждая строка это класс, а функция переопределяется

bgcolor = config.menu_bgcolor
lighted_bgcolor = config.menu_lighted_bgcolor
menu_height = config.screen_height // 2 +3
menu_width = config.menu_width
screen_width = config.screen_width
start_position_x = (screen_width - menu_width) // 2
language = config.settings['language']
suitable_keys = config.comand.values()


def get_bgcolor(lighted = False):
    color = bgcolor
    if lighted == 'lighted':
        color = lighted_bgcolor
    return color

def get_height(number):
    return menu_height + number

class Menu_button():

    def __init__(self, number, text, make):
        self.number = number
        self.text = localization.translate_text(text, language)
        self.normilized_text = self.normilize_text()
        self.make = make
        self.height = get_height(self.number)

    def normilize_text(self):
        text = self.text
        length = len(text)
        left_spaces_count = (menu_width - length) // 2
        right_spaces_count = menu_width - length - left_spaces_count
        normilized_text = ' '*left_spaces_count + text +' '*right_spaces_count
        return normilized_text

    def print(self, lighted = False):
        current_bgcolor = get_bgcolor(lighted)
        height = self.height
        text = self.normilized_text
        terminal.bkcolor(current_bgcolor)
        terminal.printf(start_position_x, height, text)
        terminal.bkcolor(bgcolor)
        terminal.refresh()


menu_button_0 = Menu_button(0, 'Start game', Game.run_game)
menu_button_1 = Menu_button(1, 'Settings', Settings.run_menu)
menu_button_2 = Menu_button(2, 'Exit', None)

buttons= [menu_button_0, menu_button_1, menu_button_2]

#Выводит на экран главное меню игры и передает управление дальше по пунктам
class Menu:
    def __init__(self, buttons):
        self.buttons = buttons
        self.length=len(self.buttons)
        self.state=0
        self.key = self.get_key()
        self.time_to_finish = False

    def view(self):
        terminal.clear()
        self.state=0
        self.buttons[0].print('lighted')
        for i in range(1,self.length):
            self.state=i
            self.buttons[i].print()
        self.state=0
        terminal.refresh()

    def get_key(self):
        key = terminal.read()
        while key not in suitable_keys:
            key = terminal.read()
        return key


    def make(self, key):
        if key == config.comand['Esc'] or key == config.comand['Close']:
            self.time_to_finish = True
        elif key == config.comand['up'] or key == config.comand['Arrow Up']:
            self.up()
        elif key == config.comand['down'] or key == config.comand['Arrow Down']:
            self.down()
        elif key == config.comand['Enter']:
            # Последняя кнопка это выход, ее номер self.len -1, остальные кнопки выполняют свои функции
            if self.state == self.length - 1:
                self.time_to_finish = True
            else:
                self.buttons[self.state].make()



    def up(self):
        self.buttons[self.state].print()
        self.state = (self.state - 1) % self.length
        self.buttons[self.state].print('lighted')


    def down(self):
        self.buttons[self.state].print()
        self.state = (self.state + 1) % self.length
        self.buttons[self.state].print('lighted')

    def run(self):
        self.view()
        while not self.time_to_finish:
            key = self.get_key()
            self.make(key)


terminal.open()
terminal.set('font: %s, size=%d;' % (config.settings['font_name'], int(config.settings['font_size'])))
menu = Menu(buttons)
menu.run()
