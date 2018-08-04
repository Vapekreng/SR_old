import os

from bearlibterminal import terminal

# comand - имя команы ('up'), key - имя клавиши, назначенной на команду ('w'), ccode - код клавиши и терминала (26)

_KEYSET_PATH = 'DATA\\keyset.txt'
_SEPARATOR = '='

_KEY_TO_CODE_DICT = dict()

_KEY_TO_CODE_DICT['a'] = terminal.TK_A
_KEY_TO_CODE_DICT['b'] = terminal.TK_B
_KEY_TO_CODE_DICT['c'] = terminal.TK_C
_KEY_TO_CODE_DICT['d'] = terminal.TK_D
_KEY_TO_CODE_DICT['e'] = terminal.TK_E
_KEY_TO_CODE_DICT['f'] = terminal.TK_F
_KEY_TO_CODE_DICT['g'] = terminal.TK_G
_KEY_TO_CODE_DICT['h'] = terminal.TK_H
_KEY_TO_CODE_DICT['i'] = terminal.TK_I
_KEY_TO_CODE_DICT['j'] = terminal.TK_J
_KEY_TO_CODE_DICT['k'] = terminal.TK_K
_KEY_TO_CODE_DICT['l'] = terminal.TK_L
_KEY_TO_CODE_DICT['m'] = terminal.TK_M
_KEY_TO_CODE_DICT['n'] = terminal.TK_N
_KEY_TO_CODE_DICT['o'] = terminal.TK_O
_KEY_TO_CODE_DICT['p'] = terminal.TK_P
_KEY_TO_CODE_DICT['q'] = terminal.TK_Q
_KEY_TO_CODE_DICT['r'] = terminal.TK_R
_KEY_TO_CODE_DICT['s'] = terminal.TK_S
_KEY_TO_CODE_DICT['t'] = terminal.TK_T
_KEY_TO_CODE_DICT['u'] = terminal.TK_U
_KEY_TO_CODE_DICT['v'] = terminal.TK_V
_KEY_TO_CODE_DICT['w'] = terminal.TK_W
_KEY_TO_CODE_DICT['x'] = terminal.TK_X
_KEY_TO_CODE_DICT['y'] = terminal.TK_Y
_KEY_TO_CODE_DICT['z'] = terminal.TK_Z
_KEY_TO_CODE_DICT['1'] = terminal.TK_1
_KEY_TO_CODE_DICT['2'] = terminal.TK_2
_KEY_TO_CODE_DICT['3'] = terminal.TK_3
_KEY_TO_CODE_DICT['4'] = terminal.TK_4
_KEY_TO_CODE_DICT['5'] = terminal.TK_5
_KEY_TO_CODE_DICT['6'] = terminal.TK_6
_KEY_TO_CODE_DICT['7'] = terminal.TK_7
_KEY_TO_CODE_DICT['8'] = terminal.TK_8
_KEY_TO_CODE_DICT['9'] = terminal.TK_9
_KEY_TO_CODE_DICT['0'] = terminal.TK_0

_UNCHANGEBLE_COMAND_TO_CODE_DICT = dict()

_UNCHANGEBLE_COMAND_TO_CODE_DICT['esc'] = terminal.TK_ESCAPE
_UNCHANGEBLE_COMAND_TO_CODE_DICT['enter'] = terminal.TK_ENTER
_UNCHANGEBLE_COMAND_TO_CODE_DICT['space'] = terminal.TK_SPACE
_UNCHANGEBLE_COMAND_TO_CODE_DICT['tab'] = terminal.TK_TAB
_UNCHANGEBLE_COMAND_TO_CODE_DICT['close'] = terminal.TK_CLOSE
_UNCHANGEBLE_COMAND_TO_CODE_DICT['arrow up'] = terminal.TK_UP
_UNCHANGEBLE_COMAND_TO_CODE_DICT['arrow down'] = terminal.TK_DOWN
_UNCHANGEBLE_COMAND_TO_CODE_DICT['arrow left'] = terminal.TK_LEFT
_UNCHANGEBLE_COMAND_TO_CODE_DICT['arrow right'] = terminal.TK_RIGHT


_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT = dict()

_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT['left'] = terminal.TK_A
_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT['right'] = terminal.TK_D
_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT['up'] = terminal.TK_W
_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT['down'] = terminal.TK_S


_DEFAULT_COMAND_TO_CODE_DICT = dict()

_DEFAULT_COMAND_TO_CODE_DICT.update(_UNCHANGEBLE_COMAND_TO_CODE_DICT)
_DEFAULT_COMAND_TO_CODE_DICT.update(_DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT)


CHANGEBLE_COMANDS = _DEFAULT_CHANGEBLE_COMAND_TO_CODE_DICT.keys()
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
        return name in CHANGEBLE_COMANDS

    def _check(self):
        all_comands_are_here = True
        used_comands = self._comand_to_code_dict.keys()
        for comand in CHANGEBLE_COMANDS:
            all_comands_are_here = all_comands_are_here and comand in used_comands
        if not all_comands_are_here:
            self._comand_to_code_dict = _DEFAULT_COMAND_TO_CODE_DICT

    def get_comands_to_code_dict(self):
        """Возвращает словарь команд"""
        return self._comand_to_code_dict

    def save(self):
        f = open(_KEYSET_PATH, 'w')
        for name in CHANGEBLE_COMANDS:
            code = self._comand_to_code_dict[name]
            key = self.convert_code_to_key_func(code)
            f.write(name + _SEPARATOR + key + '\n')
        f.close()

    @staticmethod
    def convert_code_to_key_func(code):
        new_key = ''
        for key in _KEY_TO_CODE_DICT.keys():
            if _KEY_TO_CODE_DICT[key] == code:
                new_key = key
                break
        return new_key

    def _set_code_to_comand_dict(self):
        self._code_to_comand_dict = {}
        for comand in self._comand_to_code_dict.keys():
            code = self._comand_to_code_dict[comand]
            self._code_to_comand_dict[code] = comand

    def get_code_to_comand_dict(self):
        return self._code_to_comand_dict


current_keyset = Keyset()
