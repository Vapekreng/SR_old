# TODO генерация уровней
# TODO переход между уровнями

import Map_generator, Config


# Класс, содержащий описание всей игры
class Game():
    def __init__(self, global_map=None, dungeons=None, current_level=None, quests=None, hero=None):
        self.global_map = global_map
        self.dungeons = dungeons
        self.current_dungeon = 0
        self.current_level = 0
        self.quests = quests
        self.hero = hero


# Описание подземелья: координаты выходов на глобальную картн
class Dungeons:
    def __init__(self):
        self.name = 'Test dungeon'
        self.count_of_levels = 8
        self.levels_names = ['level_0', 'level_1', 'level_2', 'level_3', 'level_4', 'level_5', 'level_6', 'level_7']
        self.levels_short_names = ['lv0', 'lv1', 'lv2', 'lv3', 'lv4', 'lv5', 'lv6', 'lv7']
        self.levels_difficalties = [0, 0, 0, 1, 1, 1, 1, 2]
        self.levels_map_types = ['rectangular', 'rectangular', 'rectangular', 'rectangular', 'rectangular',
                                 'rectangular', 'rectangular', 'rectangular']
        # Формат информации для создания лестницы: [dungeon_index, level_index, direction]. dungeon_index - номер
        # подземелья в глобальной карте. level_index - номер уровня в подземелье, direction - направление движения
        # (1 или -1). Координаты на карте следующего уровня будут сохранены после создания уровня.
        self.transition_matrix = [[[0, 1, -1]],
                                  [[0, 0, 1], [0, 2, -1]],
                                  [[0, 1, 1], [0, 3, -1], [0, 4, -1]],
                                  [[0, 2, 1], [0, 5, -1]],
                                  [[0, 2, 1], [0, 6, -1]],
                                  [[0, 3, 1], [0, 7, -1]],
                                  [[0, 4, 1], [0, 7, -1]],
                                  [[0, 5, 1], [0, 6, 1]]]
        self.levels = self.get_levels()

    # Построение карты уровня по свойствам подземелья
    # Берем первое подземелье, строим его. При построении будет лестница вниз. В классе лестницы будет указатель на
    # карту, в которую она ведет. При указании этой карты создается новая и т.д. Так пробегутся все карты
    def get_levels(self):
        pass


# Описание уровня: название, краткое название, тип карты уровня, уровень сложности, генерация карты уровня
class Levels:
    def __init__(self, name, short_name, difficalty=0, map_type='rectangular', stairs=[]):
        self.name = name
        self.short_name = short_name
        self.width = Config.screen_width
        self.height = Config.screen_height
        self.difficalty = difficalty
        # Двумерный список из символов - заготовка карты
        self.titles = Map_generator.get_map()
        self.transparent_map = self.get_transparent_map()
        self.mob_list = []
        self.icons_buffer = self.get_icons_buffer()

    def get_transparent_map(self):
        titles = self.titles
        transparent_map = []
        width = self.width
        height = self.height
        for x in range(width):
            transparent_map.append([1] * 20)
        for x in range(width):
            for y in range(height):
                transparent_map[x][y] = titles.transparent
        return transparent_map


    def get_icons_buffer(self):
        width = self.width
        height = self.height
        icons_buffer = []
        for x in range(width):
            icons_buffer.append([None] * height)
        return icons_buffer




