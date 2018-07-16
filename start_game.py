from bearlibterminal import terminal
from settings import current_settings
import main_menu

terminal.open()
font_name = current_settings.font_name
font_size = current_settings.font_size
terminal.set('font: %s, size=%d;' % (font_name, font_size))
main_menu.main_loop()
terminal.close()

