# Настройки игры: управление, экран, язык
import os

#######################################################################################################################
# Управление:


# name - имя команды
# key - клавиша команды
# code - код клавиши

# Неизменяемые команды и коды назначенных им клавиш. comand - словарь, где ключ - имя команды, а значение - код клавиши
# команды
comand = dict()
comand['esc'] = 41
comand['enter'] = 40
comand['space'] = 44
comand['tab'] = 43
comand['close'] = 224
comand['arrow up'] = 82
comand['arrow down'] = 81
comand['arrow left'] = 80
comand['arrow right'] = 79

# Настраиваемые команды и их значения по умолчанию
changeble_comands = ['left', 'right', 'up', 'down']

comand['left'] = 4
comand['right'] = 7
comand['up'] = 26
comand['down'] = 22

# Клавиши, доступные для использования
keys = ['', '', '', '', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# Получаем их числовые коды
def get_codes(keys):
    codes = dict()
    length = len(keys)
    for i in range(length):
        codes[keys[i]] = i
    return codes

codes = get_codes(keys)

#  По Имени команды получаем назначенную клавишу
def get_comand_key_from_name(comand_name):
    comand_key = 'Error'
    if comand_name in changeble_comands:
        comand_code = comand[comand_name]
        comand_key = convert_code_to_key(comand_code)
    return comand_key

# По символу клавиши получаем её код
def convert_key_to_code(key):
    if key in keys:
        return codes[key]
    else:
        return 'wrong code'

# По коду клавиши получаем её символ
def convert_code_to_key(code):
    text = None
    if type(code) is int:
        if 0<code<40:
            text = keys[code]
    return text

# загружаем из текстового файла настроек назначенные командам клавиши
def load_keyset(comand):
    # Если файл существует
    if os.path.isfile('DATA\\KeyMapping.txt'):
        f = open('DATA\\KeyMapping.txt')
        for line in f:
            # Удаляем символ окончания строки
            line = line.replace('\n', '')
            # Ищем в строке разделитель, это знак равнр
            separator = line.find('=')
            # Если знак присутствует, то
            if separator != -1:
                # Разделяем на 2 части
                string = line.split('=')
                # Имя команды - левая часть
                name = string[0].lower()
                # Удаляем пробелы
                name = name.strip()
                # Назначенная клавиша - правая часть
                key = string[1].lower()
                # Удажяем пробелы
                key = key.strip()
                # Отсеиваем случайный мусор - неверно битое имя команды
                if name in changeble_comands:
                    # по символу клавиши получаем её код
                    code = convert_key_to_code(key)
                    # Если код не занят
                    if code not in comand.values():
                        # И если клавишу можно использовать (если присутствует в keys)
                        if type(code) is int:
                            #  То назначаем новый код команде
                            comand[name] = code
        f.close()
    save_keyset(comand)


def save_keyset(comand):
    f=open('DATA\\KeyMapping.txt', 'w')
    f.write('In order to get defaults just delete this file\n')
    for name in changeble_comands:
        code = comand[name]
        key = convert_code_to_key(code)
        f.write(name + ' = ' + key + '\n')
    f.close()

def set_comand(name, key):
    name = name.strip()
    if type(key) is str:
        key = key.strip()
    if name in changeble_comands:
        if key in keys:
            code = convert_key_to_code(key)
            if code in comand.values():
                return 'This key is already busy'
            else:
                comand[name] = code
                save_keyset(comand)
                return key
            return True
        else:
            return 'Can not set this key'
    else:
        return 'Error! ' + name + ' ' + key

######################################### Настройки ####################################################################

# Язык, размер экрана, шрифт

def load_settings(settings):
    if os.path.isfile('DATA\\config.txt'):
        f = open('DATA\\config.txt')
        settings = {}
        for line in f:
            if line.find('=') != -1:
                line = line.replace(' ', '')
                line = line.replace('\n', '')
                line = line.split('=')
                name = line[0]
                settings[name] = line[1]
        f.close()
    save_settings(settings)
    return settings

def save_settings(settings):
    f = open('DATA\\config.txt', 'w')
    f.write('In order to get defaults just delete this file\n')
    for name in settings.keys():
        f.write(name + ' = ' + settings[name] + '\n')
    f.close()

def set_font_size(size):
    if int(size) > 0:
        settings['font_size'] = size
        save_settings(settings)

def set_language(new_language):
    message = 'This language do not support'
    if os.path.isfile('DATA\\localization\\en-' + new_language + '.txt'):
        message = 'Restart game to apply settings'
        settings['language'] = new_language
        save_settings(settings)
    return message

#######################################################################################################################
# Настройки экрана


screen_width = 80
screen_height=25
menu_width = 20
menu_lighted_bgcolor='dark gray'
menu_bgcolor = 'black'


#######################################################################################################################
# Настройки клавиатуры



########################################################################################################################


########################################################################################################################
# Настройки игры
# Переменная settings - словарь, где ключ - имя настройки, а значение - значение пераметра
# В переменную входят: размер шрифта, название шрифта и язык

# Значения по умолчанию
settings = dict()
settings['font_name'] = 'UbuntuMono-R.ttf'
settings['font_size'] = '18'
settings['language'] = 'en'
#######################################################################################################################


load_keyset(comand)
# обновляем значения по умолчанию
settings.update(load_settings(settings))

