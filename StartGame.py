# TODO доделать кнопки меню интерфейса.

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

# Высота экрана
screen_height = Config.screen_height

# Положение верхней кнопки меню по вертикали
menu_height = Config.screen_height // 2 + 3

# Начальное положение по горизонтали
start_position_x = (screen_width - menu_width) // 2

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
def get_key_code():
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
        self.text = Localization.translate_text(text)
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
        if key == Config.comand['esc'] or key == Config.comand['close']:
            self.time_to_exit = True
        elif key == Config.comand['up'] or key == Config.comand['arrow up']:
            self.up()
        elif key == Config.comand['down'] or key == Config.comand['arrow down']:
            self.down()
        elif key == Config.comand['enter']:
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
            key = get_key_code()
            self.make(key)

################################################ Кнопки менюшек ########################################################

# На вход подаем номер кнопки и её имя

class Sub_menu_button():
    def __init__(self, number, name, hint = ''):
        self.number = number
        self.name = name
        self.hint = self.get_hint(hint)
        self.left_text = self.get_left_text()
        self.right_text = self.get_right_text()
        self.right_text_start_position = screen_width // 2
        # Верхняя строка уходит на шапку, следующая на разделитель, а со второй строки уже идут кнопки
        self.height = 2 + self.number
        # Для каждого меню своя подсказка

    def get_left_text(self):
        text = self.name
        translated_text = Localization.translate_text(text)
        # добавляем справа пробелы для подсветки, 5, врде, нормально
        count_of_left_spases = 5
        left_spases = ' ' * count_of_left_spases
        count_of_right_spases = screen_width//2 - len(translated_text) - count_of_left_spases
        right_spases = ' ' * count_of_right_spases
        extended_text = left_spases + translated_text + right_spases
        return extended_text

    # Отличается в разных меню, так что бцдет в подклассах
    def get_right_text(self):
        pass

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

        # Подсветка текущей позиции
        current_bgcolor = get_bgcolor(lighted)
        terminal.bkcolor(current_bgcolor)

        # Сначала левую часть
        x = 0
        y = self.height
        text = self.left_text
        terminal.printf(x, y, text)

        # Потом правую
        x = self.right_text_start_position
        y = self.height
        text = self.right_text
        terminal.printf(x, y, text)

        # Возвращаем подсветку, как было
        terminal.bkcolor(bgcolor)

        # Стираем старую подсказку и печатаем новую
        self.clear_hint()
        self.print_hint()

        # И обновляем экран
        terminal.refresh()

    # Выводим на правую часть экрана сообщение
    def print_message(self, text):
        x = self.right_text_start_position
        y = self.height
        self.clear_right_text()
        centrifyed_text = self.centrify_text(text)
        terminal.printf(x, y, centrifyed_text)
        terminal.refresh()

    # Команда, выполняемая по нажатию кнопки, для каждой кнопки своя
    def make(self):
        pass

    # Очистка правой части строки
    def clear_right_text(self):
        x = self.right_text_start_position
        y = self.height
        # Заполняем пробелами правую часть строки
        text = ' ' * (screen_width//2)
        terminal.printf(x, y, text)

    # Печатаем посказку внизу экрана
    def print_hint(self):
        text = self.hint
        x = 0
        y = screen_height - 1
        terminal.printf(x, y , text)

    # Стираем подсказку
    def clear_hint(self):
        x = 0
        y = screen_height - 1
        spases = ' ' * screen_width
        terminal.printf(x, y , spases)

    # Наводим красоту на текст подсказки
    def get_hint(self, text):
        hint = Localization.translate_text(text)
        length = len(hint)
        count_of_left_spases = (screen_width - length)//2
        left_spases = ' ' * count_of_left_spases
        count_of_rightn_spases = screen_width - length - count_of_left_spases
        right_spases = ' ' * count_of_rightn_spases
        centrifyed_hint = left_spases + hint + right_spases
        return centrifyed_hint

######################################## Кнопки настроек управления ####################################################

class Keyset_menu_button(Sub_menu_button):

    def get_right_text(self):
        name = self.name
        text = Config.get_comand_key_from_name(name)
        centrified_text = self.centrify_text(text)
        return centrified_text

    # Команда, выполняемая по нажатию кнопки
    def make(self):
        self.clear_right_text()
        message = Localization.translate_text('Press any key')
        self.print_message(message)
        key_code = terminal.read();
        key = Config.convert_code_to_key(key_code)
        message = Config.set_comand(self.name, key)
        translated_message = Localization.translate_text(message)
        self.right_text = self.get_right_text()
        self.print_message(translated_message)
        if translated_message in [Localization.translate_text('This key is already busy'),
                       Localization.translate_text('Can not set this key')]:
            terminal.read()

######################################## Кнопка настройки языка #####################################################

class Game_menu_button_language(Sub_menu_button):

    def get_right_text(self):
        name = self.name
        text = Config.settings[name]
        centrified_text = self.centrify_text(text)
        return centrified_text

    # Здесь перечисляем все поддерживаемые языки
    def set_list_of_languages(self):
        self.languages = ['en', 'ru']

    # Определяем позицию текущего языка
    def get_state_of_languages(self):
        self.state_of_language = self.languages.index(Config.settings['language'])

    def next_lang(self):
        self.state_of_language = (self.state_of_language + 1) % len(self.languages)
        new_lang = self.languages[self.state_of_language]
        self.print_message(new_lang)

    def prev_lang(self):
        self.state_of_language = (self.state_of_language - 1) % len(self.languages)
        new_lang = self.languages[self.state_of_language]
        self.print_message(new_lang)

    # Команда, выполняемая по нажатию кнопки
    def make(self):
        self.set_list_of_languages()
        self.get_state_of_languages()
        self.print_message(Config.settings['language'])
        key = terminal.read()
        while key not in [Config.comand['enter'], Config.comand['esc']]:
            if key in [Config.comand['left'], Config.comand['arrow left']]:
                self.next_lang()
            if key in [Config.comand['right'], Config.comand['arrow right']]:
                self.prev_lang()
            key = terminal.read()
        if key == Config.comand['enter']:
            new_language = self.languages[self.state_of_language]
            Config.set_language(new_language)
        self.right_text = self.get_right_text()
        self.print()



############################################### Меню настроек ##########################################################

class Sub_menu():
    def __init__(self, name, buttons):
        # Заголовок меню
        translated_name = Localization.translate_text(name)
        normilized_name = '| ' + translated_name + ' |'
        self.name = normilized_name
        # Кнопки меню
        self.buttons = buttons
        # Начальная позиция
        self.state = 0
        # Количество кнопок
        self.length = len(buttons)


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

    # Нажатую клавишу получаем из Game_menu, откуда и запускается это меню
    def run(self):
        self.print()
        key = get_key_code()
        while not key in [Config.comand['esc'], Config.comand['close'], Config.comand['left'],
                          Config.comand['arrow left'], Config.comand['right'], Config.comand['arrow right']]:
            self.make(key)
            key = get_key_code()
        return key

    def make(self, key):
        if key == Config.comand['up'] or key == Config.comand['arrow up']:
            self.up()
        elif key == Config.comand['down'] or key == Config.comand['arrow down']:
            self.down()
        elif key == Config.comand['enter']:
            self.buttons[self.state].make()
            self.print()

######################################## Меню настроек игры ############################################################

# Включает в себя все меню настроек: управления, экрана и т.д.

class Game_menu():
    def __init__(self, menus):
        # Начальное положение
        self.state = 0
        self.border = '-' * screen_width
        self.menus = menus
        self.length = len(self.menus)
        self.menus_names = self.get_menus_names()
        self.menus_names_start_position = self.get_menus_names_start_positions()


    def get_menus_names(self):
        menus_names = []
        for menu in self.menus:
            new_name = menu.name
            menus_names.append(new_name)
        return menus_names

    def get_menus_names_start_positions(self):
        menus_names = self.menus_names
        menus_start_position = []
        position = 0
        for name in menus_names:
            menus_start_position.append(position)
            position += len(name)
        return menus_start_position

    def print(self):
        terminal.clear()
        x = 0
        y = 0
        for i in range(self.length):
            x = self.menus_names_start_position[i]
            y = 0
            text = self.menus_names[i]
            current_bgcolor = get_bgcolor(i == self.state)
            terminal.bkcolor(current_bgcolor)
            terminal.printf(x, y, text)
            terminal.bkcolor(bgcolor)
        # Вторая строка сверху отделяем заголовки меню от кнопок
        x = 0
        y = 1
        terminal.printf(x, y, self.border)
        # Вторая строка снизу - отделяем подсказку от кнопок
        x = 0
        y = screen_height - 2
        terminal.printf(x, y, self.border)
        terminal.refresh()

    def run(self):
        key = None
        while key not in [Config.comand['esc'], Config.comand['close']]:
            current_menu = self.menus[self.state]
            self.print()
            key = current_menu.run()
            if key == Config.comand['right'] or key == Config.comand['arrow right']:
                self.right()
                key = None
            if key == Config.comand['left'] or key == Config.comand['arrow left']:
                self.left()
                key = None

    def right(self):
        self.state = (self.state + 1) % self.length

    def left(self):
        self.state = (self.state - 1) % self.length

########################################################################################################################

# Открываем консоль, задаем шрифт и его размер.
terminal.open()
terminal.set('font: %s, size=%d;' % (font_name, font_size))

# Создаем кнопки настроек управления: налево, направо, вверх, вниз
keyset_menu_button_left = Keyset_menu_button(0, 'left', 'Press enter')
keyset_menu_button_right = Keyset_menu_button(1, 'right', 'Press enter')
keyset_menu_button_up = Keyset_menu_button(2, 'up', 'Press enter')
keyset_menu_button_down = Keyset_menu_button(3, 'down', 'Press enter')

game_menu_button_language = Game_menu_button_language(0, 'language', 'Press enter and left/right (need restart)')

# Собираем их вместе
keyset_menu_buttons = [keyset_menu_button_left, keyset_menu_button_right, keyset_menu_button_up, keyset_menu_button_down]
game_menu_buttons = [game_menu_button_language]

# Создаем подменюшки
keyset_menu = Sub_menu('Keyset menu', keyset_menu_buttons)
interface_menu = Sub_menu('Interface settings', game_menu_buttons)

# Собираем все подменюшки вместе
sub_menus = [keyset_menu, interface_menu]

# Создаем игровое меню (настройки)
game_menu = Game_menu(sub_menus)

# Задаем кнопки главного меню (стартовый экран)
main_menu_button_start_game = Main_menu_button(0, 'Start game', Game.run_game)
main_menu_button_settings = Main_menu_button(1, 'Settings', game_menu.run)
main_menu_button_exit = Main_menu_button(2, 'Exit', None)

#  Собираем их вместе
main_menu_buttons = [main_menu_button_start_game, main_menu_button_settings, main_menu_button_exit]

#  Создаем само главное меню
main_menu = Main_menu(main_menu_buttons)

#  Запускаем
main_menu.run()
