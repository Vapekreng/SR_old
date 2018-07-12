import os


class Localization:

    def __init__(self, language):
        pass



def get_localization(language):
    language = settings.settings['language']
    # Расположение файла локализации
    file_name = 'DATA\\localization\\en-' + language +'.txt'
    if os.path.isfile(file_name):
        f = open(file_name)
        for line in f:
            if line.find('=') != -1:
                line = line.strip()
                line = line.replace('\n', '')
                line = line.split('=')
                english = line[0].strip()
                translated = line[1].strip()
                localization[english] = translated
        f.close()
    return localization


# Перевод списка, результат - переведенный список
# Если перевод для элемента отсутствует в файле - оставляется английский текст
def translate_list(list):
    translated_list = list
    language = settings.settings['language']
    if language != 'en':
        length = len(list)
        for i in range(length):
            try:
                translated_list[i] = localization[list[i]]
            except KeyError:
                pass
    return translated_list


# Перевод строки, результат - переведенная строка
# Если перевод в файле отсутствует - оставляется английский текмт
def translate_text(text):
    translated_text = text
    language = settings.settings['language']
    if language != 'en':
        try:
            translated_text = localization[text]
        except KeyError:
            translated_text = text
    return translated_text

localization = get_localization(settings.settings['language'])