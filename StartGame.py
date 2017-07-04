from bearlibterminal import terminal
import Config, Game, Localization

# Цвет фона
bgcolor = Config.menu_bgcolor

# Цвет подсвеченного фона
lighted_bgcolor = Config.menu_lighted_bgcolor

# Ширина меню (то, что будет подсвечиваться)
menu_width = Config.menu_width

# Ширина экрана
screen_width = Config.screen_width

# Положение верхней кнопки меню по вертикали
menu_height = Config.screen_height // 2 + 3

# Начальное положение по горизонтали
start_position_x = (screen_width - menu_width) // 2

# Язык
language = Config.settings['language']

# Используемые в этом меню кнопки клавиатуры
suitable_keys = Config.comand.values()

# Используемый шрифт
font_name = Config.settings['font_name']

# Размер шрифта
font_size = int(Config.settings['font_size'])


# Определяем. текст выводится с подсветкой фона (для текущего меню) или нет
def get_bgcolor(lighted = False):
    color = bgcolor
    if lighted:
        color = lighted_bgcolor
    return color

# Получение допустимой команды с клавиатуры
def get_key():
    key = terminal.read()
    while key not in suitable_keys:
        key = terminal.read()
    return key


####################################### Кнопки главного меню ###########################################################

#  Кнопки главного меню. Номер, текст, выполняемая команда.
#  Текст сразу переводится и нормализуется. Вычисляется положение по вертикали.

class Main_menu_button():
    def __init__(self, number, text, make):
        self.number = number
        self.text = Localization.translate_text(text, language)
        self.normilized_text = self.normilize_text()
        self.make = make
        self.height = menu_height + self.number

    #  Меню выводится по центру с шириной, указанной в конфиге. Если подсветка только текста, то получается некрасиво,
    #  поэтому к тексту слева и справа добавляются пробелы для получения равной ширины подсветки
    def normilize_text(self):
        text = self.text
        length = len(text)
        left_spaces_count = (menu_width - length) // 2
        right_spaces_count = menu_width - length - left_spaces_count
        normilized_text = ' ' * left_spaces_count + text + ' ' * right_spaces_count
        return normilized_text

    #  Печатаем нормализованный текст кнопки, позиция по вертикали определяется номером кнопки, подсветка - передаваемым
    #  параметром
    def print(self, lighted=False):
        current_bgcolor = get_bgcolor(lighted)
        height = self.height
        text = self.normilized_text
        terminal.bkcolor(current_bgcolor)
        terminal.printf(start_position_x, height, text)
        terminal.bkcolor(bgcolor)
        terminal.refresh()


###################################### Главное меню ####################################################################

# Главное меню - переход к игре, настройкам, выход

class Main_menu:
    def __init__(self, buttons):
        self.buttons = buttons
        self.length = len(self.buttons)
        self.state = 0
        self.key = get_key()
        self.time_to_exit = False

    # Вывод всего меню на экран
    def view(self):
        terminal.clear()
        self.state = 0
        lighted = True
        self.buttons[0].print(lighted)
        for i in range(1, self.length):
            self.state = i
            self.buttons[i].print()
        self.state = 0
        terminal.refresh()

    # Выбор действия по нажатию клавиши
    def make(self, key):
        if key == Config.comand['Esc'] or key == Config.comand['Close']:
            self.time_to_exit = True
        elif key == Config.comand['up'] or key == Config.comand['Arrow Up']:
            self.up()
        elif key == Config.comand['down'] or key == Config.comand['Arrow Down']:
            self.down()
        elif key == Config.comand['Enter']:
            # Последняя кнопка это выход, ее номер self.len - 1, остальные кнопки выполняют свои функции
            if self.state == self.length - 1:
                self.time_to_exit = True
            else:
                self.buttons[self.state].make()
                self.view()

    # Переход кнопкой выше
    def up(self):
        self.buttons[self.state].print()
        self.state = (self.state - 1) % self.length
        lighted = True
        self.buttons[self.state].print(lighted)

    # Переход кнопкой ниже
    def down(self):
        self.buttons[self.state].print()
        self.state = (self.state + 1) % self.length
        lighted = True
        self.buttons[self.state].print(lighted)

    # Запуск меню
    def run(self):
        self.view()
        while not self.time_to_exit:
            key = get_key()
            self.make(key)


######################################## Кнопки меню настроек управления ###############################################

#  Кнопки меню настроек: номер, имя исполняемой команды. Текст переводится и дополняется пробелами справа и слева до
#  середины экрана (для подсветки текущей строки)

class Keyset_menu_button():
    def __init__(self, number, comand_name):
        self.number = number
        self.comand_name = comand_name
        self.left_text = self.get_left_text()
        self.right_text = self.get_right_text()
        self.right_text_start_position = screen_width // 2
        # Верхняя строка уходит на шапку, следующая на разделитель, а со второй строки уже идут кнопки
        self.height = 2 + self.number

    def get_left_text(self):
        text = self.comand_name
        translated_text = Localization.translate_text(text, language)
        centrified_text = self.centrify_text(translated_text)
        return centrified_text

    def get_right_text(self):
        comand_name = self.comand_name
        text = Config.get_comand_key_from_name(comand_name)
        centrified_text = self.centrify_text(text)
        return centrified_text

    # Выравниваем текст пробелами по центру
    def centrify_text(self, text):
        length = len(text)
        # Левая часть экрана, значит  берем половину. Оставшееся свободное место делим на 2 части
        count_of_left_spases = (screen_width // 2 - length) // 2
        # оставшееся свободное место кидаем направо
        count_of_right_spases = screen_width // 2 - length - count_of_left_spases
        centrified_text = ' ' * count_of_left_spases + text + ' ' * count_of_right_spases
        return centrified_text

    # Выводим кнопку на экран
    def print(self, lighted = False):
        # Сначала левую часть
        x = 0
        y = self.height
        text = self.left_text
        terminal.printf(x, y, text)
        # Потом правую
        current_bgcolor = get_bgcolor(lighted)
        terminal.bkcolor(current_bgcolor)
        x = self.right_text_start_position
        y = self.height
        text = self.right_text
        terminal.printf(x, y, text)
        # Возвращаем подсветку, как было
        terminal.bkcolor(bgcolor)
        # И обновляем экран
        terminal.refresh()

    # Выводим на правую часть экрана сообщение
    def print_message(self, text):
        x = self.right_text_start_position
        y = self.height
        self.clear_right_text()
        terminal.printf(x, y, text)

    # Команда, выполняемая по нажатию кнопки
    def make(self):
        self.clear_right_text()
        message = Localization.translate_text('press any key')
        self.print_message(message)
        key = get_key();
        message = Config.set_comand(self.comand_name, key)
        self.print_message(message)

    # Очистка правой части строки
    def clear_right_text(self):
        x = self.right_text_start_position
        y = self.height
        # Заполняем пробелами правую часть строки
        text = ' ' * (screen_width//2)
        terminal.printf(text, x, y)

######################################## Меню настроек управления #####################################################

class Keyset_menu():
    def __init(self, buttons):
        # Заголовок меню
        name = 'Keyset menu'
        translated_name = Localization.translate_text(name, language)
        normilized_name = '| ' + translated_name + ' |'
        self.name = normilized_name
        # Подсказка
        hint = 'Press Enter to change value'
        translated_hint = Localization.translate_text(hint, language)
        centrified_hint = self.centrify_text(translated_hint)
        self.hint = centrified_hint
        # Кнопки меню
        self.buttons = buttons
        # Начальная позиция
        self.state = 0
        # Количество кнопок
        self.length = len(buttons)
        # Условие выхода из меню
        self.time_to_exit = False

    def print(self):
        for button in self.buttons:
            # Если номер кнопки совпадает с номером активной позиции меню, то подсвечиваем
            button.print(self.state == button.number)

    def up(self):
        button = self.buttons[self.state]
        button.print()
        self.state = (self.state - 1) % self.length
        lighted = True
        button = self.buttons[self.state]
        button.print(lighted)

    def down(self):
        button = self.buttons[self.state]
        button.print()
        self.state = (self.state + 1) % self.length
        lighted = True
        button = self.buttons[self.state]
        button.print(lighted)

    def run(self):
        self.print()
        while not self.time_to_exit:
            key = get_key()
            self.make(key)

    def make(self, key):
        if key == Config.comand['Esc'] or key == Config.comand['Close']:
            self.time_to_exit = True
        elif key == Config.comand['up'] or key == Config.comand['Arrow Up']:
            self.up()
        elif key == Config.comand['down'] or key == Config.comand['Arrow Down']:
            self.down()
        elif key == Config.comand['Enter']:
            # Последняя кнопка это выход, ее номер self.len - 1, остальные кнопки выполняют свои функции
            self.buttons[self.state].make()
            self.view()

######################################## Меню настроек игры ############################################################

# Включает в себя все меню настроек: управления, экрана и т.д.

class Game_menu():
    def __init__(self, menues):
        # Начальное положение
        self.state = 0




# TODO Собрать кнопки в меню настроек управления, сделать класс меню настроек управления. Сделать кнопки основного меню:
# TODO  размер шрифта и язык, ну и само основное меню

# Открываем консоль, задаем шрифт и его размер.
terminal.open()
terminal.set('font: %s, size=%d;' % (font_name, font_size))

# Создаем кнопки настроек управления: налево, направо, вверх, вниз

keyset_menu_button_left = Keyset_menu_button(0, 'left')
keyset_menu_button_right = Keyset_menu_button(1, 'right')
keyset_menu_button_up = Keyset_menu_button(0, 'up')
keyset_menu_button_down = Keyset_menu_button(0, 'down')

# Собираем их вместе и создаем меню настроек

keyset_menu_buttons = [keyset_menu_button_left, keyset_menu_button_right, keyset_menu_button_up, keyset_menu_button_down]
keyset_menu = Keyset_menu(keyset_menu_buttons)

#  Задаем кнопки главного меню
main_menu_button_start_game = Main_menu_button(0, 'Start game', Game.run_game)
main_menu_button_settings = Main_menu_button(1, 'Settings', Settings.run_menu)
main_menu_button_exit = Main_menu_button(2, 'Exit', None)

#  Собираем их вместе
main_menu_buttons = [main_menu_button_start_game, main_menu_button_settings, main_menu_button_exit]

#  Создаем само главное меню
main_menu = Main_menu(main_menu_buttons)

#  Запускаем
main_menu.run()
