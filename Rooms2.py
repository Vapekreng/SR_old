# Разбиваем всю карту на ячейки, в каждой ячейке строим комнату
# TODO Для высокой или широкой комнаты дублировать координаты в массиве комнат
# TODO Сделать массив коридоров и стен комнат (или не надо?), или сделать стены комнат их частью?

import Config, random
from bearlibterminal import terminal

screen_width = Config.screen_width
screen_height = Config.screen_height
font_name = Config.settings['font_name']
font_size = int(Config.settings['font_size'])

# Количество ячеек по х и у
cell_x = 4
cell_y = 2

# Ширина ячеек по х и у
step_x = screen_width // cell_x
# Сверху оставлено 2 строки для текста, снизу 3 строки для характеристик
step_y = (screen_height - 5) // cell_y

# Минимальные и максимальные размеры комнат
room_width_min = 8
room_width_max = 14
room_height_min = 3
room_height_max = 6

# Создание начальной большой комнаты
class Map:
    def __init__(self):
        self.titles = self.make_titles_list()
        self.rooms = self.make_rooms_list()
        self.passages = []

    # Сначала все тайтлы - стены (#)
    def make_titles_list(self):
        titles = []
        for x in range(80):
            line = []
            for y in range(20):
                line.append('#')
            titles.append(line)
        return titles

    # Комнаты хранятся в двумерном массиве, для начала заполняем его минус единицами
    def make_rooms_list(self):
        rooms = []
        for x in range(cell_x):
            line = []
            for y in range(cell_y):
                line.append(-1)
            rooms.append(line)
        print(rooms)
        return rooms


    # Выводит на экран карту: границы, комнаты и прилегающие стены
    def print(self):
        for x in range(80):
            for y in range(20):
                if self.room_is_near(x, y):
                    terminal.printf(x, y + 2, map.titles[x][y])

    # Проверяет, является ли клетка границей, частью комнаты или стеной комнаты
    def room_is_near(self, x, y):
        answer = False
        titles = self.titles
        # Это комната
        if titles[x][y] == '.':
            answer = True
        else:
            # Это границы подземелья
            if x == 0 or x == 79 or y == 0 or y == 19:
                answer = True
            else:
                # Проверяем соседние клетки, если найдем часть комнаты: '.' значит тут у нас стена
                if '.' in [titles[x - 1][y - 1], titles[x - 1][y], titles[x - 1][y + 1], titles[x][y - 1],
                           titles[x][y + 1], titles[x + 1][y - 1], titles[x + 1][y], titles[x + 1][y + 1]]:
                    answer = True
        return answer

    # room - список из 4 элементов, содержащий координаты левого верхнего и правого нижнего углов комнаты
    def add_room(self, room, room_index_x, room_index_y):
        x0 = room[0]
        x1 = room[1]
        y0 = room[2]
        y1 = room[3]
        # Добавляем тайтлы к карте
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                self.titles[x][y] = '.'
        # Добавляем комнату к карте
        self.rooms[room_index_x][room_index_y] = room

    # Проверяет, будут ли стены соседних комнат соприкасаться и правим координаты, если нужно
    # Проверяем комнаты слева и сверху, в том числе наискосок
    def check_close_wall(self, room, room_index_x, room_index_y):
        x = room[0]
        y = room[1]
        # Если комната не самая левая - проверяем комнату слева
        if room_index_x != 0:
            x_prev = self.rooms[room_index_x - 1][room_index_y][2]
            if x - x_prev == 3:
                x = x + 1
        # Если комната не самая верхняя, то проверяем комнату сверху
        if room_index_y != 0:
            y_prev = self.rooms[room_index_x][room_index_y - 1][3]
            if y - y_prev == 3:
                y = y + 1

        # Не самая левая и не самая верхняя - проверяем комнату наискосок
        if (room_index_x != 0) and (room_index_y != 0):
            if x - x_prev == 3:
                x = x + 1
            if y - y_prev == 3:
                y = y + 1
        room[0] = x
        room[1] = y
        return room

# х0 и у0 - координаты левого верхнего угла ячейки, в которой строим комнату

def get_room(x0, y0):
    # К шиирине и высоте добавляем 2 - на стены
    width = random.randint(room_width_min, room_width_max) + 2
    height = random.randint(room_height_min, room_height_max) + 2
    x1 = x0 + random.randint(0, step_x - width)
    x2 = x1 + width - 1
    y1 = y0 + random.randint(0, step_y - height)
    y2 = y1 + height - 1
    # Все координаты сдвигаем к центру комнаты - это стены
    return [x1 + 1, y1 + 1, x2 - 1, y2 - 1]

terminal.open()
terminal.set('font: %s, size=%d;' % (font_name, font_size))

map = Map()
for x in range(cell_x):
    for y in range(cell_y):
        room = get_room(x * step_x, y * step_y)
        # TODO переделать входные данные на массивы, чтобы не прописывать кучу переменных и индексы
        checked_room = map.check_close_wall(room, x, y)
        map.add_room(checked_room, x, y)
map.print()
terminal.refresh()
terminal.read()
print(map.rooms)
