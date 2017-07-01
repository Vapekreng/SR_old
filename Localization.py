# Получает перевод из файла локализации
# По умолчанию английский язык
# Все переводы с английского
# Файл перевода имеет имя en-ln.txt и распологается в папке /DATA/localization
# Формат строки перевода:
# Текст на английском = текст на другом языке
# Перевод хранится в переменной localization, которая представляет собой словарь

import Config, os
language = Config.settings['language']
localization = dict()


# Получение перевода на заданный язык
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


# Перевод списка, результат - переведенный список
# Если перевод для элемента отсутствует в файле - оставляется английский текст
def translate_list(list, language):
    translated_list = list
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
def translate_text(text, language):
    translated_text = text
    if language != 'en':
        try:
            translated_text = localization[text]
        except KeyError:
            translated_text = text
    return translated_text

localization = get_localization(language)
