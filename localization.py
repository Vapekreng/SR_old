import os
import settings

LOCALIZATION_PATH = 'DATA\\localization\\en-'
LOCALIZATION_PATH_LAST_SYMBOLS = '.txt'
TRANSLATE_SEPARATOR = '='
DEFAULT_LANGUAGE = 'en'


class Localization:

    def __init__(self):
        self.language = settings.current_settings.language
        self.localization = {}
        self._set()

    def change_language(self, new_language):
        if self._language_is_correct(new_language):
            self.language = new_language
            settings.current_settings.set_language(new_language)
            self._set()

    def translate(self, text):
        if text in self.localization.keys():
            return self.localization[text]
        return text

    @staticmethod
    def _language_is_correct(new_language):
        if type(new_language) is not str:
            return False
        if not os.path.isfile(LOCALIZATION_PATH + new_language + LOCALIZATION_PATH_LAST_SYMBOLS):
            return False
        return True

    def _set(self):
        path = self._get_path()
        new_localization = {}
        if os.path.isfile(path):
            f = open(path, 'r')
            new_localization = self._pars_file(f)
            f.close()
        self.localization = new_localization

    def _get_path(self):
        path = LOCALIZATION_PATH + self.language + LOCALIZATION_PATH_LAST_SYMBOLS
        return path

    def _pars_file(self, f):
        new_localization = {}
        for line in f:
            original, translated = self._pars_line(line)
            new_localization[original] = translated
        return new_localization

    @staticmethod
    def _pars_line(line):
        original, translated = '', ''
        if line.find(TRANSLATE_SEPARATOR) != -1:
            line = line.replace('\n', '')
            line = line.strip()
            splitted = line.split(TRANSLATE_SEPARATOR)
            original, translated = splitted[0].strip(), splitted[1].strip()
        return original, translated


current_localization = Localization()
