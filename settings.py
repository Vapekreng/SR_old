FONT_SIZE = 24
FONT_NAME = 'UbuntuMono-R.ttf'
LANGUAGE = 'en'

class Settings:

    def __init__(self):
        self.font_size = FONT_SIZE
        self.font_name = FONT_NAME
        self.language = LANGUAGE
        self.get_settings()

    def get_settings(self):
        pass

    def save_sattings(self):
        pass


current_settings = Settings()