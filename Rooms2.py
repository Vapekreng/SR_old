import Config, random
from bearlibterminal import terminal

screen_width = Config.screen_width
screen_height = Config.screen_height

map_width = screen_width
# Высота карты равна высоте экрана минус 5, так как сверху оставляю 2 строки для текста, а снизу 3 строки для информации
map_height = screen_height - 5

font_name = Config.settings['font_name']
font_size = int(Config.settings['font_size'])

# Карта состоит из тайтлов - 1 тайтл это 1 символ
# Разбиваем всю карту на ячейки, в каждой ячейке строим комнату. У меня размер ячеек 10 на 10 тайтлов (карта размером
# 80 на 20, соответственно 8 ячеек по горизонтали и 2 по вертикали)

# Количество ячеек по х и у
cell_count_x = 8
cell_count_y = 2

# Ширина ячеек по х и у
min_cell_width = map_width // cell_count_x
min_cell_height = map_height // cell_count_y

# room_types - минимальные и максимальные размеры прямоугольных комнат. Содержатся в словаре. Ключ - тип,
# значение - список. По порядку: минимальная ширина - максимальная ширина - минимальная высота - максимальная высота
# Cell_type - типы ячеек и их ширина и высота.
# Максимальная высота и ширина комнаты НЕ ДОЛЖНА ПРЕВЫШАТЬ высоту и ширину выделенных под нее ячеек

room_types = dict()
cell_types = dict()

# Обычная комната - 2 ячейки в ширину и одна в высоту
room_types['normal'] = [8, 14, 3, 6]
cell_types['normal'] = [2 * min_cell_width, min_cell_height]

# Маленькая комната 1 на 1 ячейку
room_types['small'] = [3, 6, 3, 6]
cell_types['small'] = [min_cell_width, min_cell_height]

# Высокая комната - 1 ячейка в ширину и 2 в высоту
room_types['high'] = [6, 8, 8, 14]
cell_types['high'] = [min_cell_width, 2 * min_cell_height]

# Широкая комната - 3 клетки в ширину и 1 в высоту
room_types['wide'] = [12, 16, 3, 6]
cell_types['wide'] = [3 * min_cell_width, min_cell_height]



# Строим прямоугольную комнату. Входные данные: тип комнаты, тип занимаемой ячейки, адрес ячейки
class Rectangular_room:
    def __init__(self, room_type, cell_type,  x, y):
        self.type = 'rectangular'
        self.cell_type = cell_type
        # Координаты левой верхней ячейки комнаты
        self.cell_index_x = x
        self.cell_index_y = y
        self.coord = self.get_room_coord(room_type, cell_type)

    def get_room_coord(self, room_type, cell_type):
        x = self.cell_index_x
        y = self.cell_index_y
        # Вычисляем координаты левого верхнего угла ячейки карты
        corner_x = x * min_cell_width
        corner_y = y * min_cell_height
        # По типу комнаты определяем диапазоны ширины и высоты комнаты
        new_room_type = room_types[room_type]
        min_width = new_room_type[0]
        max_width = new_room_type[1]
        min_heigt = new_room_type[2]
        max_heigh = new_room_type[3]
        # Находим ширину и высоту комнаты, +2 добавляем на стены, в конце уберем
        room_width = random.randint(min_width, max_width) + 2
        room_height = random.randint(min_heigt, max_heigh) + 2
        # Находим ширину и высоту ячейки
        cell_width = cell_types[cell_type][0]
        cell_height = cell_types[cell_type][1]
        x0 = corner_x + random.randint(0, cell_width - room_width)
        y0 = corner_y + random.randint(0, cell_height - room_height)
        x1 = x0 + room_width - 1
        y1 = y0 + room_height - 1
        # Все координаты сдвигаем к центру комнаты - это стены
        return [x0 + 1, y0 + 1, x1 - 1, y1 - 1]

# Контейнер для клеток и комнат
class Map:
    def __init__(self):
        self.titles = self.make_titles_list()
        self.rooms = self.make_rooms_list()

    # Сначала все тайтлы - стены (#)
    def make_titles_list(self):
        titles = []
        for x in range(80):
            line = []
            for y in range(20):
                line.append('#')
            titles.append(line)
        return titles

    def get_titles(self):
        for cell_x in range(cell_count_x):
            for cell_y in range(cell_count_y):
                room = self.rooms[cell_x][cell_y]
                if room != 'free':
                    x0 = room.coord[0]
                    y0 = room.coord[1]
                    x1 = room.coord[2]
                    y1 = room.coord[3]
                    # Добавляем тайтлы к карте
                    for x in range(x0, x1 + 1):
                        for y in range(y0, y1 + 1):
                            self.titles[x][y] = '.'


    # Комнаты хранятся в двумерном массиве, для начала заполняем его минус единицами
    def make_rooms_list(self):
        rooms = []
        for x in range(cell_count_x):
            line = []
            for y in range(cell_count_y):
                line.append('free')
            rooms.append(line)
        return rooms


    # Добавляем к карте комнату. Входные данные - комната, координаты левой верхней ячейки комнаты
    def add_room(self, room):
        # Добавляем комнату к карте
        x = room.cell_index_x
        y = room.cell_index_y
        self.rooms[x][y] = room

    # Проверяет, будут ли стены соседних комнат соприкасаться и правим координаты, чтобы их развести
    def check_close_wall(self):
        # Сначала проверим по столбцам: берем нулевой столбец и сверяем с первым, потом первый со вторым и.т.д.
        for x in range(cell_count_x - 1):
            if self.check_left_column(x):
                self.correct_column(x + 1)

        #  Аналогично со строками
        for y in range(cell_count_y - 1):
            if self.check_upper_line(y):
                self.correct_line(y + 1)

    def check_left_column(self, x):
        answer = False
        right_border_index = (x + 1) * min_cell_width - 2
        for y in range(cell_count_y):
            room = self.rooms[x][y]
            if room != 'free':
                right_x = room.coord[2]
                if right_x == right_border_index:
                    answer = True
        return answer

    def correct_column(self, x):
        left_border_index = x * min_cell_width + 1
        for y in range(cell_count_y):
            room = self.rooms[x][y]
            if room != 'free':
                left_x = room.coord[0]
                if left_x == left_border_index:
                    self.rooms[x][y].coord[0] += 1

    def check_upper_line(self, y):
        answer = False
        lower_border_index = (y + 1) * min_cell_height - 2
        for x in range(cell_count_x):
            room = self.rooms[x][y]
            if room != 'free':
                low_y = room.coord[3]
                if low_y == lower_border_index:
                    answer = True
        return answer

    def correct_line(self, y):
        upper_border_index = y * min_cell_height + 1
        for x in range(cell_count_x):
            room = self.rooms[x][y]
            if room != 'free':
                upper_y = room.coord[1]
                if upper_y == upper_border_index:
                    self.rooms[x][y].coord[1] += 1

    # Выводит на экран карту: границы, комнаты и прилегающие стены
    def print(self):
        for x in range(map_width):
            for y in range(map_height):
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
            if x == 0 or x == map_width - 1  or y == 0 or y == map_height - 1:
                answer = True
            else:
                # Проверяем соседние клетки, если найдем часть комнаты: '.' значит тут у нас стена. Выхода за пределы
                # списка не будет, так как границы проверили выше
                if '.' in [titles[x - 1][y - 1], titles[x - 1][y], titles[x - 1][y + 1], titles[x][y - 1],
                           titles[x][y + 1], titles[x + 1][y - 1], titles[x + 1][y], titles[x + 1][y + 1]]:
                    answer = True
        return answer

terminal.open()
terminal.set('font: %s, size=%d;' % (font_name, font_size))

map = Map()
for x in range(0, 4):
    for y in range(cell_count_y):
        room = Rectangular_room('normal', 'normal', 2 * x, y)
        map.add_room(room)
map.check_close_wall()
map.get_titles()
map.print()
terminal.refresh()
terminal.read()
