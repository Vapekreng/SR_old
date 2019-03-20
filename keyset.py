import pickle

from bearlibterminal import terminal

import localization as lk
from settings import settings

# comand - имя команы ('up'), key - имя клавиши, назначенной на команду ('w'), ccode - код клавиши и терминала (26)

KEYSET_PATH = 'DATA\\keyset.sav'

KEYS = dict()

KEYS[terminal.TK_A] = 'a'
KEYS[terminal.TK_B] = 'b'
KEYS[terminal.TK_C] = 'c'
KEYS[terminal.TK_D] = 'd'
KEYS[terminal.TK_E] = 'e'
KEYS[terminal.TK_F] = 'f'
KEYS[terminal.TK_G] = 'g'
KEYS[terminal.TK_H] = 'h'
KEYS[terminal.TK_I] = 'i'
KEYS[terminal.TK_J] = 'j'
KEYS[terminal.TK_K] = 'k'
KEYS[terminal.TK_L] = 'l'
KEYS[terminal.TK_M] = 'm'
KEYS[terminal.TK_N] = 'n'
KEYS[terminal.TK_O] = 'o'
KEYS[terminal.TK_P] = 'p'
KEYS[terminal.TK_Q] = 'q'
KEYS[terminal.TK_R] = 'r'
KEYS[terminal.TK_S] = 's'
KEYS[terminal.TK_T] = 't'
KEYS[terminal.TK_U] = 'u'
KEYS[terminal.TK_V] = 'v'
KEYS[terminal.TK_W] = 'w'
KEYS[terminal.TK_X] = 'x'
KEYS[terminal.TK_Y] = 'y'
KEYS[terminal.TK_Z] = 'z'
KEYS[terminal.TK_1] = '1'
KEYS[terminal.TK_2] = '2'
KEYS[terminal.TK_3] = '3'
KEYS[terminal.TK_4] = '4'
KEYS[terminal.TK_5] = '5'
KEYS[terminal.TK_6] = '6'
KEYS[terminal.TK_7] = '7'
KEYS[terminal.TK_8] = '8'
KEYS[terminal.TK_9] = '9'
KEYS[terminal.TK_0] = '0'
KEYS[terminal.TK_KP_1] = 'NumLock 1'
KEYS[terminal.TK_KP_2] = 'NumLock 2'
KEYS[terminal.TK_KP_3] = 'NumLock 3'
KEYS[terminal.TK_KP_4] = 'NumLock 4'
KEYS[terminal.TK_KP_5] = 'NumLock 5'
KEYS[terminal.TK_KP_6] = 'NumLock 6'
KEYS[terminal.TK_KP_7] = 'NumLock 7'
KEYS[terminal.TK_KP_8] = 'NumLock 8'
KEYS[terminal.TK_KP_9] = 'NumLock 9'
KEYS[terminal.TK_KP_0] = 'NumLock 0'


class Keyset():

    def __init__(self):
        self.codes = {}
        self.codes['up'] = terminal.TK_KP_8
        self.codes['ur'] = terminal.TK_KP_9
        self.codes['right'] = terminal.TK_KP_6
        self.codes['dr'] = terminal.TK_KP_3
        self.codes['down'] = terminal.TK_KP_2
        self.codes['dl'] = terminal.TK_KP_1
        self.codes['left'] = terminal.TK_KP_4
        self.codes['ul'] = terminal.TK_KP_7
        self.keys = KEYS

    def save(self):
        f = open(KEYSET_PATH, 'wb')
        pickle.dump(self, f)
        f.close()

    def load(self):
        try:
            f = open(KEYSET_PATH, 'rb')
            data = pickle.load(f)
            f.close()
        except FileNotFoundError:
            data = self
            self.save()
        return data

    def change_code(self, old_code, new_code):
        language = settings.language
        if new_code not in KEYS.keys():
            answer = lk.WRONG_KEY[language]
        elif new_code in self.codes.values():
            answer = lk.KEY_IS_BUSY[language]
        else:
            key = self.find_key(old_code)
            self.codes[key] = new_code
            answer = KEYS[new_code]
            self.save()
        return answer

    def find_key(self, code):
        answer = None
        for key in self.codes.keys():
            if self.codes[key] == code:
                answer = key
                break
        return answer


keyset = Keyset()
keyset = keyset.load()