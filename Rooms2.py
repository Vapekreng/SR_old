# TODO соединение комнат коридорами
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

# type_sizes - размеры (в минимальных ячейках карты) комнат или ячеек

types_sizes = dict()
types_sizes['normal'] = [2, 1]
types_sizes['small'] = [1, 1]
types_sizes['high'] = [1, 2]
types_sizes['wide'] = [3, 1]
types_sizes['square'] = [2, 2]

# cell_types - список всех типов ячеек
# cell_type_features - типы ячеек и их ширина и высота.
# Максимальная высота и ширина комнаты НЕ ДОЛЖНА ПРЕВЫШАТЬ высоту и ширину выделенных под нее ячеек
# 1 * пишу, чтобы сразу было видно размер ячеек

cell_types = ['normal', 'small', 'high', 'wide', 'square']

cell_type_features = dict()
cell_type_features['normal'] = [2 * min_cell_width, 1 * min_cell_height]
cell_type_features['small']  = [1 * min_cell_width, 1 * min_cell_height]
cell_type_features['high']   = [1 * min_cell_width, 2 * min_cell_height]
cell_type_features['wide']   = [3 * min_cell_width, 1 * min_cell_height]
cell_type_features['square'] = [2 * min_cell_width, 2 * min_cell_height]

# room_types - список всех типов ячеек
# room_type_features - минимальные и максимальные размеры прямоугольных комнат. Содержатся в словаре. Ключ - тип,
# значение - список. По порядку: минимальная ширина - максимальная ширина - минимальная высота - максимальная высота
# appropriate_cells - типы ячеек, которые могут вместить комнату. Ширина и высота комнаты должна быть как минимум на 2
# меньше, чем ширина и высота выделенных под нее ячеек, так как 2 тайтла уходят на стены
# room_chance - шанс выпадения этой комнаты

room_types = ['normal', 'small', 'high', 'wide', 'square']

room_types_features = dict()
appropriate_cells = dict()

# Обычная комната - 2 ячейки в ширину и одна в высоту
room_types_features['normal'] = [9, 15, 4, 7]
appropriate_cells['normal'] = ['normal', 'wide', 'square']

# Маленькая комната 1 на 1 ячейку
room_types_features['small'] = [6, 8, 6, 8]
appropriate_cells['small'] = ['normal', 'small', 'high', 'wide', 'square']

# Высокая комната - 1 ячейка в ширину и 2 в высоту
room_types_features['high'] = [7, 8, 8, 13]
appropriate_cells['high'] = ['high', 'square']

# Широкая комната - 3 клетки в ширину и 1 в высоту
room_types_features['wide'] = [19, 27, 4, 7]
appropriate_cells['wide'] = ['wide']

# Квадратная комната 2 на 2
room_types_features['square'] = [13, 17, 9, 13]
appropriate_cells['square'] = ['square']

# Словарь, содержащий вероятность выбора того или иного типа. Для себя сделал так, чтобы сумма была равна 100, но это
# не обязательно
dict_of_chances = dict()
dict_of_chances['normal'] = 30
dict_of_chances['small']  = 5
dict_of_chances['high']   = 25
dict_of_chances['wide']   = 35
dict_of_chances['square'] = 5

# Словарь для вывода карты на экран

titles_icons = dict()
titles_icons['border'] = '#'
titles_icons['wall'] = '#'
titles_icons['border and wall'] = '#'
titles_icons['free'] = ''
titles_icons['room'] = '.'
titles_icons['passage'] = '.'
titles_icons['door'] = '+'

# Словарь для замены тайтлов проведенного коридора

passage_dict = dict()
passage_dict['wall'] = 'door'
passage_dict['free'] = 'passage'
passage_dict['room'] = 'room'

# Строим прямоугольную комнату. Входные данные: тип комнаты, тип занимаемой ячейки, адрес ячейки
class Rectangular_room:
    def __init__(self, room_type,  x, y):
        self.name = 'rectangular'
        self.room_type = room_type
        # Координаты левой верхней ячейки комнаты
        self.cell_index_x = x
        self.cell_index_y = y
        self.coord = self.get_room_coord()

    def get_room_coord(self):
        x = self.cell_index_x
        y = self.cell_index_y
        room_type = self.room_type
        # Вычисляем координаты левого верхнего угла ячейки карты
        corner_x = x * min_cell_width
        corner_y = y * min_cell_height
        # По типу комнаты определяем диапазоны ширины и высоты комнаты
        new_room_features = room_types_features[room_type]
        min_width = new_room_features[0]
        max_width = new_room_features[1]
        min_heigt = new_room_features[2]
        max_heigh = new_room_features[3]
        # Находим ширину и высоту комнаты, +2 добавляем на стены, в конце уберем
        room_width = random.randint(min_width, max_width) + 2
        room_height = random.randint(min_heigt, max_heigh) + 2
        # Находим ширину и высоту ячейки
        cell_width = cell_type_features[room_type][0]
        cell_height = cell_type_features[room_type][1]
        x0 = corner_x + random.randint(0, cell_width - room_width)
        y0 = corner_y + random.randint(0, cell_height - room_height)
        x1 = x0 + room_width - 2
        y1 = y0 + room_height - 2
        # Все координаты сдвигаем к центру комнаты - это стены
        return [x0 + 1, y0 + 1, x1 - 1, y1 - 1]

# Контейнер для клеток и комнат
class Map:
    def __init__(self):
        self.titles = self.make_titles_list()
        self.rooms = []
        self.cells = self.make_cells_list()

    # Сначала все тайтлы - стены (#)
    def make_titles_list(self):
        titles = []
        for x in range(map_width):
            line = []
            for y in range(map_height):
                if x in [0, map_width - 1] or y in [0, map_height - 1]:
                    line.append('border')
                else:
                    line.append('free')
            titles.append(line)
        return titles

    def get_titles(self):
        for room in self.rooms:
            x0 = room.coord[0]
            y0 = room.coord[1]
            x1 = room.coord[2]
            y1 = room.coord[3]
            # Добавляем тайтлы комнат и их стен к карте
            for x in range(x0 - 1, x1 + 2):
                for y in range(y0 - 1, y1 + 2):
                    if x in [x0 - 1, x1 + 1] or y in [y0 - 1, y1 + 1]:
                        if self.titles[x][y] != 'border':
                            self.titles[x][y] = 'wall'
                        else:
                            self.titles[x][y] = 'border and wall'
                    else:
                        self.titles[x][y] = 'room'

    # Двумерный список ячеек карты, первоначально все ячейки свободные (True)
    def make_cells_list(self):
        cells = []
        for x in range(cell_count_x):
            line = []
            for y in range(cell_count_y):
                line.append(True)
            cells.append(line)
        return cells

    # Добавляем к карте комнату.
    def add_room(self, room):
        self.rooms.append(room)

    # Выводит на экран карту: границы, комнаты и прилегающие стены для просмотра
    def print(self):
        for x in range(map_width):
            for y in range(map_height):
                if self.titles[x][y]:
                    title = self.titles[x][y]
                    icon = titles_icons[title]
                    terminal.printf(x, y + 2, icon)

    # Проверяет, свободны ли ячейки карты для данного типа
    def check_spase_for_type(self, checked_type, x0, y0):
        size_x = types_sizes[checked_type][0]
        size_y = types_sizes[checked_type][1]
        answer = True
        for x in range(x0, x0 + size_x):
            for y in range(y0, y0 + size_y):
                try:
                    if self.cells[x][y] == False:
                        answer = False
                except IndexError:
                    answer = False
        return answer


    # Случайным образом, в соответствии с вероятностью room_chances, выбираем тип комнаты с учетом свободных ячеек на
    # карте
    def get_room_type(self, x, y):
        # Собираем все типы комнат, которые могут поместиться на карте
        appropriate_types = []
        for room_type in room_types:
            if self.check_spase_for_type(room_type, x, y):
                appropriate_types.append(room_type)
        # Строим таблицу вероятности для выбранных типов
        chance_list = []
        full_chance = 0
        # Берем первый тип комнаты - прибавляем её вероятность к полной вероятности. Это будет пороговое значение для
        # этой комнаты. Добавляем это значение в chance_list. и так далее по всем типам комнат
        for current_type in appropriate_types:
            full_chance += dict_of_chances[current_type]
            chance_list.append(full_chance)
        # Берем случайное значение от 0 до full_chance - 1 и ищем, на какую ячейку оно попало
        n = random.randint(0, full_chance - 1)
        room_type = None
        for i in range(len(appropriate_types)):
            if n < chance_list[i]:
                room_type = appropriate_types[i]
                break
        return room_type

    # Помечаем ячейки, как занятые
    def mark_cells_as_busy(self, x0 ,y0, room_type):
        size_x = types_sizes[room_type][0]
        size_y = types_sizes[room_type][1]
        for x in range(x0, x0 + size_x):
            for y in range(y0, y0 + size_y):
                self.cells[x][y] = False

    # Получаем случайную карту, наполненную прямоугольными комнатами
    def get_rectangular_map(self):
        for y in range(cell_count_y):
            for x in range(cell_count_x):
                if self.cells[x][y]:
                    room_type = self.get_room_type(x, y)
                    self.mark_cells_as_busy(x, y, room_type)
                    room = Rectangular_room(room_type, x, y)
                    self.add_room(room)
        self.get_titles()

    # Прокладываем коридор от точки (x0, y0) до точки (x1, y1)
    def get_passage(self, x0, y0, x1, y1):
        if x0 == x1 and y0 == y1:
            return []
        pass_map = self.get_pass_map()
        check_map = self.get_check_map()
        # step - номер шага, им будем маркировать проверенные ячейки и потом в обратном порядке возвращаться, получая
        # путь
        check_map[x0][y0] = 0
        wave = [[x0, y0]]
        step = 1
        front, check_map = self.get_front(wave, check_map, pass_map, step)
        while [x1, y1] not in front and front != []:
            step += 1
            wave = front
            front, check_map = self.get_front(wave, check_map, pass_map, step)
        passage = []
        if [x1, y1] in front:
            passage = self.get_way_back(check_map, step, [x1, y1], [x0, y0])
        self.add_passage_to_map(passage)

    # Получение карты проходимости. В данный момент для коридора годятся клетки стен, комнат и свободные клетки
    def get_pass_map(self):
        cells = []
        for x in range(map_width):
            line = []
            for y in range(map_height):
                if self.titles[x][y] in ['wall', 'room', 'free']:
                    line.append(True)
                else:
                    line.append(False)
            cells.append(line)
        return cells

    # Получение карты ячеек, которые нужно проверить. Первоначально все ячейки -1 - требуют проверки
    def get_check_map(self):
        cells = []
        for x in range(map_width):
            line = []
            for y in range(map_height):
                line.append(-1)
            cells.append(line)
        return cells

    # Получаем фронт волны - соседние ячейки
    def get_front(self, wave, check_map, pass_map, step):
        front = []
        for title in wave:
            x0 = title[0]
            y0 = title[1]
            # diff - изменение координат точки, берем только движение по прямой, не наискосок
            for diff in [[1, 0], [0, -1], [-1, 0], [0, 1]]:
                x = x0 + diff[0]
                y = y0 + diff[1]
                if pass_map[x][y] and (check_map[x][y] == -1):
                    front.append([x, y])
                    check_map[x][y] = step
        return front, check_map

    # Прокладываем путь от конечной точки к начальной и получаем коридор
    def get_way_back(self, check_map, step, finish, start):
        passage = []
        current_point = finish
        passage.append(current_point)
        for i in range(step):
            for diff in [[1, 0], [0, -1], [-1, 0], [0, 1]]:
                x = current_point[0] + diff[0]
                y = current_point[1] + diff[1]
                if check_map[x][y] == step - i:
                    current_point = [x, y]
                    passage.append(current_point)
        passage.append(start)
        return passage

    # Добавляем коридор к тайтлам карты
    def add_passage_to_map(self, passage):
        # Сначала добавляем коридор
        for titles in passage:
            x = titles[0]
            y = titles[1]
            self.titles[x][y] = passage_dict[self.titles[x][y]]
        # А потом стены вокруг него
        for titles in passage:
            x = titles[0]
            y = titles[1]
            self.add_passages_walls(x, y)

    def add_passages_walls(self, x0 ,y0):
        for diff in [[-1, 1], [-1, 0], [-1, -1], [0, 1], [0, -1], [1, 1], [1, 0], [1,- 1]]:
            x = x0 + diff[0]
            y = y0 + diff[1]
            if self.titles[x][y] == 'free':
                self.titles[x][y] = 'wall'

terminal.open()
terminal.set('font: %s, size=%d;' % (font_name, font_size))
map = Map()
map.get_rectangular_map()
passage = map.get_passage(11, 11, 55, 15)
map.print()
terminal.refresh()
terminal.read()