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
changeble_comands = ['left', 'right', 'up', 'down']
general_settings = ['font_size']

# Неизменяемые команды и значения по умолчанию
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


# Шрифт и размер шрифта по умолчанию
settings = dict(zip(['font_name', 'font_size'], ['UbuntuMono-R.ttf', '18']))

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
            #Delete spases and end of line
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            separator = line.find('=')
            if separator != -1:
                string = line.split('=')
                name = string[0].lower()
                key = string[1].lower()
                if name in changeble_comands:
                    code = convert_key_to_code(key)
                    if code not in comand.values():
                        if code != 'wrong code':
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

def set_comand(comand, name, key):
    name = name.strip()
    key = key.strip()
    if name in changeble_comands:
        if key in keys:
            code = convert_key_to_code(key)
            if code in comand.values():
                return 'Эта клавиша уже занята'
            else:
                comand[name] = code
                save_keyset(comand)
                return key
            return True
        else:
            return 'Клавиша не может быть задана'
    else:
        return 'Error! ' + name + ' ' + key


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
        f.write(name + '=' + settings[name] + '\n' )
    f.close()


def set_font_size(size):
    if int(size )> 0:
        settings['font_size'] = size
        save_settings(settings)


load_keyset(comand)
settings.update(load_settings(settings))

