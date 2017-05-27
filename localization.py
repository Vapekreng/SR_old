# Получает перевод из файла локализации
import config, os
language = config.settings['language']
localization = dict()


def get_localization(language):
    # Расположение файла локализации
    file_name = 'DATA\\localization\\en-' + language +'.txt'
    if os.path.isfile(file_name):
        f = open(file_name)
        for line in f:
            if line.find('#') == -1:
                line = line.strip()
                line = line.replace('\n', '')
                line = line.split('=')
                english = line[0]
                translated = line[1]
                localization[english] = translated
        f.close()
    return localization


def translate_list(list):
    length = len(list)
    translated_list = []
    for i in range(length):
        translated_list.append(localization[list[i]])
    return translated_list


localization = get_localization(language)
