# Комната - прямоугольник из клеток пола. первоначально вся карта за исключением границ - одна большая комната. Потом
# выбираем самую большую по площади комнату и делим рандомом надвое. Так продолжаем несколько раз. Узкие комнаты
# переделываем в стены

# TODO Попробовать: выбираем самую большую незанятую область и создаем в ней комнату с рандомными размерами.
# TODO Вероятность размеров по икс и игрек задать таблицей через функцию распределения
# TODO Добавить проверку больших пустых пространств и добавление комнаты при необходимости

import Config, random
from bearlibterminal import terminal

screen_width = Config.screen_width
screen_height = Config.screen_height
font_name = Config.settings['font_name']
font_size = int(Config.settings['font_size'])

# Создание начальной большой комнаты
class Rooms:
    def __init__(self, x0 = 1, y0 = 1, x1 = screen_width - 2, y1 = screen_height - 7):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.dx = x1-x0
        self.dy = y1 - y0
        self.area = self.dx * self.dy

    # Минимальная ширина комнаты у меня 3, поэтому комнаты делятся только если размерность 7 или больше. Делится по
    # большей размерности (в данный момент приоритет по у в 2 раза)

    def separate(self):
        dx = self.dx
        dy = self.dy
        new_x0 = new_x2 = self.x0
        new_x1 = new_x3 = self.x1
        new_y0 = new_y2 = self.y0
        new_y1 = new_y3 = self.y1
        # Приоритет деления по вертикали, при условии, что размер позволяет
        if (dx > 2 * dy) or (dy < 7):
            n = random.randint(new_x0 + 3, new_x1 - 3)
            new_x1 = n - 1
            new_x2 = n + 1
        else:
            n = random.randint(new_y0 + 3, new_y1 - 3)
            new_y1 = n - 1
            new_y2 = n + 1
        new_x0 += random.randint(0, 1)
        new_x1 -= random.randint(0, 1)
        new_y0 += random.randint(0, 1)
        new_y1 -= random.randint(0, 1)
        new_x2 += random.randint(0, 1)
        new_x3 -= random.randint(0, 1)
        new_y2 += random.randint(0, 1)
        new_y3 -= random.randint(0, 1)
        new_room_1 = Rooms(new_x0, new_y0, new_x1, new_y1)
        new_room_2 = Rooms(new_x2, new_y2, new_x3, new_y3)
        return [new_room_1, new_room_2]

# Печатает всё стенами, потом по верху клетки пола для каждой комнаты
def print_rooms(list_of_rooms):
    for i in range(20):
        terminal.printf(0, i, 80 * '#')
    for room in list_of_rooms:
        for x in range(room.x0, room.x1+1):
            for y in range(room.y0, room.y1+1):
                terminal.printf(x, y, '.')

# Ищет номер максимальной по площади комнаты
def find_max(list_of_rooms):
    max_area = 0
    max_index = 0
    count_of_rooms = len(list_of_rooms)
    for i in range(count_of_rooms):
        if list_of_rooms[i].area > max_area:
            max_area = list_of_rooms[i].area
            max_index = i
    return max_index

# Удаляет из списка комнаты с шириной меньше или равной 2
def delete_thin_rooms(list_of_rooms):
    list_for_delete = []
    count_of_rooms = len(list_of_rooms)
    for i in range(count_of_rooms):
        room = list_of_rooms[i]
        if (room.dx <= 2) or (room.dy <= 2):
            list_for_delete.append(i)
    for i in range(count_of_rooms, -1, -1):
        if i in list_for_delete:
            list_of_rooms.pop(i)
    return list_of_rooms

# Из списка комнат создает двумерный массив - карту уровня
# TODO Сделать классом, добавить в аргументы номер комнаты (для дальнейшей постройки коридоров)
def get_map(list_of_rooms):
    map = []
    for x in range(80):
        map.append(['#'] * 20)
    for room in list_of_rooms:
        for x in range(room.x0, room.x1+1):
            for y in range(room.y0, room.y1+1):
                map[x][y] = '.'
    return map

# Выводит на экран карту: границы, комнаты и прилегающие стены
def print_map(map):
    for x in range(80):
        for y in range(20):
            if room_is_near(map, x, y):
                terminal.printf(x, y, map[x][y])

# Проверяет, является ли клетка границей, частью комнаты или стеной комнаты
def room_is_near(map, x, y):
    answer = False
    if map[x][y] == '.':
        answer = True
    else:
        if x == 0 or x == 79 or y == 0 or y == 19:
            answer = True
        else:
            if '.' in [map[x - 1][y - 1], map[x - 1][y], map[x - 1][y + 1], map[x][y - 1], map[x][y + 1],
                       map[x + 1][y - 1], map[x + 1][y], map[x + 1][y + 1]]:
                answer = True
    return answer


terminal.open()
terminal.set('font: %s, size=%d;' % (font_name, font_size))

room = Rooms()
list_of_rooms = [room]
for i in range(9):
    max = find_max(list_of_rooms)
    new_rooms = list_of_rooms[max].separate()
    list_of_rooms.pop(max)
    list_of_rooms.append(new_rooms[0])
    list_of_rooms.append(new_rooms[1])
    list_of_rooms = delete_thin_rooms(list_of_rooms)
map = get_map(list_of_rooms)
print_map(map)
terminal.refresh()
terminal.read()

