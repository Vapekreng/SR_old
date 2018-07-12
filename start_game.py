from bearlibterminal import terminal
from settings import current_settings
from main_menu import MainMenu

terminal.open()
font_name = current_settings.font_name
font_size = current_settings.font_size
terminal.set('font: %s, size=%d;' % (font_name, font_size))
main_menu = MainMenu()
main_menu.run_loop()

