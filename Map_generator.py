# TODO В комнатах маркировать непроходимыми только по 3 угловые клетки на каждом углу или даже по одной
# TODO При добавлении двери делать соседние стены непроходимыми
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

# type_sizes - размеры (в минимальных ячейках карты) комнат

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
cell_type_features['small'] = [1 * min_cell_width, 1 * min_cell_height]
cell_type_features['high'] = [1 * min_cell_width, 2 * min_cell_height]
cell_type_features['wide'] = [3 * min_cell_width, 1 * min_cell_height]
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
dict_of_chances['small'] = 5
dict_of_chances['high'] = 25
dict_of_chances['wide'] = 35
dict_of_chances['square'] = 5

# Словарь для вывода карты на экран - замена названий на значки

titles_icons = dict()
titles_icons['border'] = '#'
titles_icons['wall'] = '#'
titles_icons['border and wall'] = '#'
titles_icons['free'] = ''
titles_icons['room'] = '.'
titles_icons['passage'] = '.'
titles_icons['door'] = '+'
titles_icons['unpassable wall'] = '#'

# Словарь для замены тайтлов проведенного коридора

passage_dict = dict()
passage_dict['wall'] = 'door'
passage_dict['free'] = 'passage'
passage_dict['room'] = 'room'
passage_dict['unpassable wall'] = 'unpassable wall'


############################################ Построение прямоугольных комнат ###########################################

# Строим прямоугольную комнату. Входные данные: тип комнаты, тип занимаемой ячейки, адрес ячейки
class RectangularRoom:
    def __init__(self, room_type, x, y):
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


####################################### Задаем класс карты  ############################################################

# Контейнер для клеток и комнат
class Map:
    def __init__(self):
        self.titles = self.make_titles_list()
        self.rooms = []
        self.cells = self.make_cells_list()

    # Сначала все тайтлы - free или border (границы уровня)
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

    # Двумерный список ячеек карты, первоначально все ячейки свободные (True)
    def make_cells_list(self):
        cells = []
        for x in range(cell_count_x):
            line = []
            for y in range(cell_count_y):
                line.append(True)
            cells.append(line)
        return cells

##################################### Заполняем карту прямоугольными комнатами #########################################

    # Получаем случайную карту, наполненную прямоугольными комнатами
    def get_rectangular_rooms(self):
        for y in range(cell_count_y):
            for x in range(cell_count_x):
                if self.cells[x][y]:
                    room_type = self.get_room_type(x, y)
                    self.mark_cells_as_busy(x, y, room_type)
                    room = RectangularRoom(room_type, x, y)
                    self.add_room(room)
        self.get_titles()

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

    # Проверяет, свободны ли ячейки карты для данного типа
    def check_spase_for_type(self, checked_type, x0, y0):
        size_x = types_sizes[checked_type][0]
        size_y = types_sizes[checked_type][1]
        answer = True
        for x in range(x0, x0 + size_x):
            for y in range(y0, y0 + size_y):
                try:
                    if not self.cells[x][y]:
                        answer = False
                except IndexError:
                    answer = False
        return answer

    # Помечаем ячейки, как занятые
    def mark_cells_as_busy(self, x0, y0, room_type):
        size_x = types_sizes[room_type][0]
        size_y = types_sizes[room_type][1]
        for x in range(x0, x0 + size_x):
            for y in range(y0, y0 + size_y):
                self.cells[x][y] = False

    # Добавляем к карте комнату.
    def add_room(self, room):
        self.rooms.append(room)

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

######################################## Маркируем углы комнат непроходимыми ###########################################

    # Делается это для того, чтобы коридор не прошел по стене или её части и не изменил комнату (например, слил 2
    # комнаты в однуВ комнатах координаты углов задают координаты ПУСТОГО пространства, а не стен, так что для стен
    # координаты будут изменены в сторону от центра
    def set_unpassable_walls(self):
        for room in self.rooms:
            x0 = room.coord[0] - 1
            y0 = room.coord[1] - 1
            x1 = room.coord[2] + 1
            y1 = room.coord[3] + 1
            self.titles[x0][y0] = 'unpassable wall'
            self.titles[x1][y0] = 'unpassable wall'
            self.titles[x0][y1] = 'unpassable wall'
            self.titles[x1][y1] = 'unpassable wall'

############################################ Соединяем комнаты коридорами ##############################################

    # Создаем сеть коридоров (net), связывающую все комнаты вместе. Для начала берем последнюю комнату, добавляем её в
    # список net - в нем будут храниться уже связанные комнаты, потом берем случайную из оставшихся и соединяем центры
    # комнат коридором
    def make_net(self):
        rooms = self.rooms
        count_of_rooms_in_net = 0
        count_of_rooms_not_in_net = len(rooms)
        if count_of_rooms_not_in_net > 1:
            net = [rooms[count_of_rooms_not_in_net - 1]]
            rooms.pop(count_of_rooms_not_in_net - 1)
            count_of_rooms_in_net += 1
            count_of_rooms_not_in_net -= 1
            while count_of_rooms_not_in_net > 0:
                # Номер комнаты не в сети
                n1 = random.randint(0, count_of_rooms_not_in_net - 1)
                x1, y1 = self.get_center_of_room(rooms[n1])
                # Ищем номер ближайшей комнаты в сети для комнаты с центром в точке x1, y1
                n2 = self.get_closest_room(x1, y1, net)
                # Соединяем середины этих 2 комнат
                x2, y2 = self.get_center_of_room(net[n2])
                # Соединяем комнаты
                self.get_passage(x1, y1, x2, y2)
                # Добавляем комнату в сеть, убираем из несоединенных, тикаем счетчики
                net.append(rooms[n1])
                rooms.pop(n1)
                count_of_rooms_in_net += 1
                count_of_rooms_not_in_net -= 1

    # Ищем координаты центра комнаты
    def get_center_of_room(self, room):
        x0 = room.coord[0]
        y0 = room.coord[1]
        x1 = room.coord[2]
        y1 = room.coord[3]
        x = (x0 + x1) // 2
        y = (y0 + y1) // 2
        return x, y

    # Для точки x1, y1 ищем ближайшую комнату в сети
    def get_closest_room(self, x1, y1, net):
        x2, y2 = self.get_center_of_room(net[0])
        min_dist = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
        n = 0
        count_of_rooms_in_net = len(net)
        if count_of_rooms_in_net > 1:
            for i in range(1, count_of_rooms_in_net):
                x2, y2 = self.get_center_of_room(net[i])
                dist = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
                if dist < min_dist:
                    min_dist = dist
                    n = i
        return n

    #Прокладываем коридор от точки (x0, y0) до точки (x1, y1)
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

    # Добавляем коридор к тайтлам карты. Помечаем стены, прилегающие к дверям, как непроходимые
    def add_passage_to_map(self, passage):
        # Сначала добавляем коридор
        for titles in passage:
            x = titles[0]
            y = titles[1]
            self.titles[x][y] = passage_dict[self.titles[x][y]]
            # Если ставим дверь, то впритык нам еще 1 дверь не нужна, так что помечаем соседние стены непроходимыми
            if self.titles[x][y] == 'door':
                for diff in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                    dx = diff[0]
                    dy = diff[1]
                    if self.titles[x + dx][y + dy] == 'wall':
                        self.titles[x + dx][y + dy] = 'unpassable wall'
        # А потом стены вокруг него
        for titles in passage:
            x = titles[0]
            y = titles[1]
            self.add_passages_walls(x, y)

    # Каждую вторую стену коридора помечаем непроходимой, чтобы коридоры не сливались
    def add_passages_walls(self, x0, y0):
        for diff in [[-1, 1], [-1, 0], [-1, -1], [0, 1], [0, -1], [1, 1], [1, 0], [1, - 1]]:
            x = x0 + diff[0]
            y = y0 + diff[1]
            if self.titles[x][y] == 'free':
                # Сумма координат четная -> помечаем непроходимой стеной, иначе - обыкновенная стена
                if (x + y) % 2 == 0:
                    self.titles[x][y] = 'unpassable wall'
                else:
                    self.titles[x][y] = 'wall'

############################################ Вывод карты на экран ######################################################

    # Выводит на экран карту: границы, комнаты и прилегающие стены для просмотра
    def print(self):
        for x in range(map_width):
            for y in range(map_height):
                title = self.titles[x][y]
                icon = titles_icons[title]
                terminal.printf(x, y + 2, icon)


terminal.open()
terminal.set('font: %s, size=%d;' % (font_name, font_size))
new_map = Map()
new_map.get_rectangular_rooms()
new_map.set_unpassable_walls()
new_map.make_net()
new_map.print()
terminal.refresh()
terminal.read()
