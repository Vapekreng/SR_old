import os

LOCALIZATION_PATH = '\\DATA\\localization\\en-'
TRANSLATE_SEPARATOR = '='


class Localization:

    def __init__(self, language):
        self.language = language
        self.localization = self._set_localization()

    def change_language(self, new_language):
        if self._new_language_is_correct(new_language):
            self.language = new_language
            self._set_localization()

    @staticmethod
    def _new_language_is_correct(new_language):
        if type(new_language) is not str:
            return False
        if not os.path.isdir(LOCALIZATION_PATH + new_language):
            return False
        return True

    def _set_localization(self):
        localization_path = self._get_localization_path()
        new_localization = {}
        if os.path.isfile(localization_path):
            f = open(localization_path, 'r')
            new_localization = self._get_localization_from_file(f)
            f.close()
        return new_localization

    def _get_localization_path(self):
        localization_path = LOCALIZATION_PATH + self.language
        return localization_path

    def _get_localization_from_file(self, f):
        new_localization = {}
        for line in f:
            original, translated = self._get_translate_from_line(line)
            new_localization[original] = translated
        return new_localization

    @staticmethod
    def _get_translate_from_line(line):
        original, splitted = '', ''
        if line.find(TRANSLATE_SEPARATOR) != -1:
            line.replace('\n', '')
            line.strip()
            splitted_line = line.split(TRANSLATE_SEPARATOR)
            original, translated = splitted_line[0], splitted_line[1]
        return original, splitted
