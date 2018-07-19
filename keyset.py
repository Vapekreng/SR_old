import os

# comand - имя команы ('up'), key - имя клавиши, назначенной на команду ('w'), ccode - код клавиши и терминала (26)

_KEYSET_PATH = 'DATA\\keyset.txt'
_SEPARATOR = '='

_KEY_TO_CODE_DICT = dict()

_KEY_TO_CODE_DICT['a'] = 4
_KEY_TO_CODE_DICT['b'] = 5
_KEY_TO_CODE_DICT['c'] = 6
_KEY_TO_CODE_DICT['d'] = 7
_KEY_TO_CODE_DICT['e'] = 8
_KEY_TO_CODE_DICT['f'] = 9
_KEY_TO_CODE_DICT['g'] = 10
_KEY_TO_CODE_DICT['h'] = 11
_KEY_TO_CODE_DICT['i'] = 12
_KEY_TO_CODE_DICT['j'] = 13
_KEY_TO_CODE_DICT['k'] = 14
_KEY_TO_CODE_DICT['l'] = 15
_KEY_TO_CODE_DICT['m'] = 16
_KEY_TO_CODE_DICT['n'] = 17
_KEY_TO_CODE_DICT['o'] = 18
_KEY_TO_CODE_DICT['p'] = 19
_KEY_TO_CODE_DICT['q'] = 20
_KEY_TO_CODE_DICT['r'] = 21
_KEY_TO_CODE_DICT['s'] = 22
_KEY_TO_CODE_DICT['t'] = 23
_KEY_TO_CODE_DICT['u'] = 24
_KEY_TO_CODE_DICT['v'] = 25
_KEY_TO_CODE_DICT['w'] = 26
_KEY_TO_CODE_DICT['x'] = 27
_KEY_TO_CODE_DICT['y'] = 28
_KEY_TO_CODE_DICT['z'] = 29
_KEY_TO_CODE_DICT['1'] = 30
_KEY_TO_CODE_DICT['2'] = 31
_KEY_TO_CODE_DICT['3'] = 32
_KEY_TO_CODE_DICT['4'] = 33
_KEY_TO_CODE_DICT['5'] = 34
_KEY_TO_CODE_DICT['6'] = 35
_KEY_TO_CODE_DICT['7'] = 36
_KEY_TO_CODE_DICT['8'] = 37
_KEY_TO_CODE_DICT['9'] = 38
_KEY_TO_CODE_DICT['0'] = 39

_UNCHANGEBLE_COMAND_TO_CODE_DICT = dict()

_UNCHANGEBLE_COMAND_TO_CODE_DICT['esc'] = 41
_UNCHANGEBLE_COMAND_TO_CODE_DICT['enter'] = 40
_UNCHANGEBLE_COMAND_TO_CODE_DICT['space'] = 44
_UNCHANGEBLE_COMAND_TO_CODE_DICT['tab'] = 43
_UNCHANGEBLE_COMAND_TO_CODE_DICT['close'] = 224
_UNCHANGEBLE_COMAND_TO_CODE_DICT['arrow up'] = 82
_UNCHANGEBLE_COMAND_TO_CODE_DICT['arrow down'] = 81
_UNCHANGEBLE_COMAND_TO_CODE_DICT['arrow left'] = 80
_UNCHANGEBLE_COMAND_TO_CODE_DICT['arrow right'] = 79


_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT = dict()

_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT['left'] = 4
_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT['right'] = 7
_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT['up'] = 26
_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT['down'] = 22


_DEFAULT_COMAND_TO_CODE_DICT = dict()

_DEFAULT_COMAND_TO_CODE_DICT.update(_UNCHANGEBLE_COMAND_TO_CODE_DICT)
_DEFAULT_COMAND_TO_CODE_DICT.update(_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT)


CHANGEBLE_COMAND_TO_CODE_DICT = _DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT.keys()
_USABLE_KEYS = _KEY_TO_CODE_DICT.keys()
_USABLE_CODES = _KEY_TO_CODE_DICT.values()


class Keyset:

    def __init__(self):
        """Создание класса для настроек управления"""
        self._comand_to_code_dict = {}
        self._code_to_comand_dict = {}
        if self._keyset_is_exist():
            self._load()
        self._comand_to_code_dict.update(_UNCHANGEBLE_COMAND_TO_CODE_DICT)
        self._check()
        self._set_code_to_comand_dict()
        self.save()

    @staticmethod
    def _keyset_is_exist():
        return os.path.isfile(_KEYSET_PATH)

    def _load(self):
        f = open(_KEYSET_PATH, 'r')
        for line in f:
            comand, key = self._pars(line)
            self.set_comand_to_code(comand, key)

    @staticmethod
    def _pars(line):
        comand, key = '', ''
        if line.find(_SEPARATOR) != -1:
            line = line.replace('\n', '')
            parsed = line.split('=')
            comand = parsed[0].lower()
            comand = comand.strip()
            key = parsed[1].lower()
            key = key.strip()
        return comand, key

    def set_comand_to_code(self, comand, key):
        """Задает для команы comand код клавиши key"""
        if self._key_is_good(key) and self._comand_is_good(comand):
            code = _KEY_TO_CODE_DICT[key]
            self._comand_to_code_dict[comand] = code
            self._set_code_to_comand_dict()

    def _key_is_good(self, key):
        if key not in _USABLE_KEYS:
            return False
        code = _KEY_TO_CODE_DICT[key]
        return code not in self._comand_to_code_dict.values()

    @staticmethod
    def _comand_is_good(name):
        return name in CHANGEBLE_COMAND_TO_CODE_DICT

    def _check(self):
        all_comands_are_here = True
        used_comands = self._comand_to_code_dict.keys()
        for comand in CHANGEBLE_COMAND_TO_CODE_DICT:
            all_comands_are_here = all_comands_are_here and comand in used_comands
        if not all_comands_are_here:
            self._comand_to_code_dict = _DEFAULT_COMAND_TO_CODE_DICT

    def get_comands_to_code_dict(self):
        """Возвращает словарь команд"""
        return self._comand_to_code_dict

    def save(self):
        f = open(_KEYSET_PATH, 'w')
        for name in CHANGEBLE_COMAND_TO_CODE_DICT:
            code = self._comand_to_code_dict[name]
            key = self.convert_code_to_key_func(code)
            f.write(name + _SEPARATOR + key + '\n')
        f.close()

    @staticmethod
    def convert_code_to_key_func(code):
        key = ''
        for key in _KEY_TO_CODE_DICT.keys():
            if _KEY_TO_CODE_DICT[key] == code:
                key = key
                break
        return key

    def _set_code_to_comand_dict(self):
        self._code_to_comand_dict = {}
        for comand in self._comand_to_code_dict.keys():
            code = self._comand_to_code_dict[comand]
            self._code_to_comand_dict[code] = comand

    def get_code_to_comand_dict(self):
        return self._code_to_comand_dict


current_keyset = Keyset()
