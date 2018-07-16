import os

_KEYSET_PATH = 'DATA\\keyset.txt'
_SEPARATOR = '='

_KEY_CODES = dict()

_KEY_CODES['a'] = 4
_KEY_CODES['b'] = 5
_KEY_CODES['c'] = 6
_KEY_CODES['d'] = 7
_KEY_CODES['e'] = 8
_KEY_CODES['f'] = 9
_KEY_CODES['g'] = 10
_KEY_CODES['h'] = 11
_KEY_CODES['i'] = 12
_KEY_CODES['j'] = 13
_KEY_CODES['k'] = 14
_KEY_CODES['l'] = 15
_KEY_CODES['m'] = 16
_KEY_CODES['n'] = 17
_KEY_CODES['o'] = 18
_KEY_CODES['p'] = 19
_KEY_CODES['q'] = 20
_KEY_CODES['r'] = 21
_KEY_CODES['s'] = 22
_KEY_CODES['t'] = 23
_KEY_CODES['u'] = 24
_KEY_CODES['v'] = 25
_KEY_CODES['w'] = 26
_KEY_CODES['x'] = 27
_KEY_CODES['y'] = 28
_KEY_CODES['z'] = 29
_KEY_CODES['1'] = 30
_KEY_CODES['2'] = 31
_KEY_CODES['3'] = 32
_KEY_CODES['4'] = 33
_KEY_CODES['5'] = 34
_KEY_CODES['6'] = 35
_KEY_CODES['7'] = 36
_KEY_CODES['8'] = 37
_KEY_CODES['9'] = 38
_KEY_CODES['0'] = 39

_UNCHANGEBLE_COMANDS = dict()

_UNCHANGEBLE_COMANDS['esc'] = 41
_UNCHANGEBLE_COMANDS['enter'] = 40
_UNCHANGEBLE_COMANDS['space'] = 44
_UNCHANGEBLE_COMANDS['tab'] = 43
_UNCHANGEBLE_COMANDS['close'] = 224
_UNCHANGEBLE_COMANDS['arrow up'] = 82
_UNCHANGEBLE_COMANDS['arrow down'] = 81
_UNCHANGEBLE_COMANDS['arrow left'] = 80
_UNCHANGEBLE_COMANDS['arrow right'] = 79


_DEFAULT_CHANGEBLE_COMANDS = dict()

_DEFAULT_CHANGEBLE_COMANDS['left'] = 4
_DEFAULT_CHANGEBLE_COMANDS['right'] = 7
_DEFAULT_CHANGEBLE_COMANDS['up'] = 26
_DEFAULT_CHANGEBLE_COMANDS['down'] = 22


_DEFAULT_COMANDS = dict()

_DEFAULT_COMANDS.update(_UNCHANGEBLE_COMANDS)
_DEFAULT_COMANDS.update(_DEFAULT_CHANGEBLE_COMANDS)


_CHANGEBLE_COMANDS = _DEFAULT_CHANGEBLE_COMANDS.keys()
_USABLE_KEYS = _KEY_CODES.keys()
_USABLE_CODES = _KEY_CODES.values()


class Keyset:

    def __init__(self):
        """Создание класса для настроек управления"""
        self.comands = dict()
        if self._keyset_is_exist():
            self._load()
        self.comands.update(_UNCHANGEBLE_COMANDS)
        self._check()
        self.save()

    @staticmethod
    def _keyset_is_exist():
        return os.path.isfile(_KEYSET_PATH)

    def _load(self):
        f = open(_KEYSET_PATH, 'r')
        for line in f:
            name, key = self._pars(line)
            self.set_comand(name, key)

    @staticmethod
    def _pars(line):
        name, key = '', ''
        if line.find(_SEPARATOR) != -1:
            line = line.replace('\n', '')
            parsed = line.split('=')
            name = parsed[0].lower()
            name = name.strip()
            key = parsed[1].lower()
            key = key.strip()
        return name, key

    def set_comand(self, name, key):
        """Задает для команы name клавишу key"""
        if self._key_is_good(key) and self._name_is_good(name):
            code = _KEY_CODES[key]
            self.comands[name] = code

    def _key_is_good(self, key):
        if key not in _USABLE_KEYS:
            return False
        code = _KEY_CODES[key]
        return code not in self.comands.values()

    @staticmethod
    def _name_is_good(name):
        return name in _CHANGEBLE_COMANDS

    def _check(self):
        all_comands_are_here = True
        used_comands = self.comands.keys()
        for comand in _CHANGEBLE_COMANDS:
            all_comands_are_here = all_comands_are_here and comand in used_comands
        if not all_comands_are_here:
            self.comands = _DEFAULT_COMANDS

    def get_comands(self):
        """Возвращает словарь команд"""
        return self.comands

    def save(self):
        f = open(_KEYSET_PATH, 'w')
        for name in _CHANGEBLE_COMANDS:
            code = self.comands[name]
            key = self._convert_code_to_key(code)
            f.write(name + _SEPARATOR + key + '\n')
        f.close()

    def _convert_code_to_key(self, code):
        key = ''
        for key in _KEY_CODES.keys():
            if _KEY_CODES[key] == code:
                key = key
                break
        return key

current_keyset = Keyset()