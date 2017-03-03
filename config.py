import os

screen_width = 80
screen_height=25
menu_width = 20
menu_lighted_bgcolor='dark gray'
menu_bgcolor = 'black'

# name - имя команды
# key - клавиша команды
# code - код клавиши

#Настраиваемые клавиши
keys = ['', '', '', '', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# Их числовые коды
codes = dict()
for i in range(40):
    codes[keys[i]] = i

# Их имена
names = ['left', 'right', 'up', 'down']

#неизменяемые команды и значения по умолчанию
comand = dict()
comand['Esc'] = 41
comand['Enter'] = 40
comand['Space'] = 44
comand['Tab'] = 43
comand['Close'] = 224
comand['Arrow Up'] = 82
comand['Arrow Down'] = 81
comand['Arrow Left'] = 80
comand['Arrow Right'] = 79
comand['left'] = 4
comand['right'] = 7
comand['up'] = 26
comand['down'] = 22

def convert_key_to_code(key):
    if key in keys:
        return codes[key]
    else:
        return 'wrong key'

def convert_code_to_key(code):
    if 0<code<40:
        return keys[code]
    else:
        return 'wrong code'


def load_keyset(comand):
    if os.path.isfile('DATA\\KeyMapping.txt'):
        f = open('DATA\\KeyMapping.txt')
        for line in f:
            separator = line.find('=')
            if separator != -1:
                name = line[0:separator]
                name = name.strip()
                name = name.lower()
                key = line[separator + 1:]
                key = key.strip()
                key = key.lower()
                if name in names:
                    code = convert_key_to_code(key)
                    if code not in comand.values():
                        if code != 'wrong code':
                            comand[name] = code
        f.close()
    else:
        save_keyset(comand)

def save_keyset(comand):
    f=open('DATA/KeyMapping.txt', 'w')
    for name in names:
        code = comand[name]
        key = convert_code_to_key(code)
        f.write(name + ' = ' + key + '\n')
    f.close()

def set_comand(comand, name, key):
    if name in names and key in keys:
        code = convert_key_to_code(key)
        comand[name] = code
        save_keyset(comand)

load_keyset(comand)
settings = dict()
f = open('DATA/config.txt')
for line in f:
    separator = line.find(':')
    # Ищем знак двоеточия
    name = line[0:separator]
    # До двоеточия - имя переменной
    # В конце строки символ окончания строки - откидываем его. В конфиге ОБЯЗАТЕЛЬНО пустая строка в конце
    settings[name] = line[separator + 2:-1]
    # После двоеточия - значение, закрыть файл настроек
f.close()
