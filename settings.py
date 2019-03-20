import pickle
from bearlibterminal import terminal
import localization as lk

SETTINGS_PATH = 'DATA\\settings.sav'
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 100


class Settings():

    def __init__(self):
        self.font_size = 24
        self.font_name = 'UbuntuMono-R.ttf'
        self.language = lk.RU

    def save(self):
        f = open(SETTINGS_PATH, 'wb')
        pickle.dump(self, f)
        f.close()

    def load(self):
        try:
            f = open(SETTINGS_PATH, 'rb')
            data = pickle.load(f)
            f.close()
        except FileNotFoundError:
            data = self
            self.save()
        return data

    def set_font_size(self, new_font_size):
        self.font_size = new_font_size
        self.save()
        terminal.set('font: %s, size=%d;' % (self.font_name, self.font_size))

    def set_language(self, new_language):
        self.language = new_language
        self.save()

settings = Settings()
settings = settings.load()
