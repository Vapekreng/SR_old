# TODO генерация уровней
# TODO переход между уровнями


import Map_generator

# Описание подземелья: координаты выходов на глобальную картн
class Dungeons:
    def __init__(self):
        # Первые 2 значения пустые, позиция координат совпадала с номером выхода в матрице смежности
        self.name = 'Test dungeon'
        self.exit_to_the_global_map = [[], [], [5, 5]]
        self.count_of_levels = 8
        self.levels_names = ['level_0', 'level_1', 'level_2', 'level_3', 'level_4', 'level_5', 'level_6', 'level_7']
        self.levels_short_names = ['lv0', 'lv1', 'lv2', 'lv3', 'lv4', 'lv5', 'lv6', 'lv7']
        self.levels_difficalties = [0, 0, 0, 1, 1, 1, 1, 2]
        self.levels_map_types = ['rectangular', 'rectangular', 'rectangular', 'rectangular', 'rectangular',
                                 'rectangular', 'rectangular', 'rectangular']
        self.transition_matrix = [[2, 1, 0, 0, 0, 0, 0, 0], [-1, 0 ,1, 0, 0, 0, 0, 0],
                                      [0, -1, 0, 1, 0, 1, 0, 0], [0, 0, -1, 0, 1, 0, 0, 0], [0, 0, 0, -1, 0, 0, 0, 1],
                                      [0, 0, -1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, -1, 0, 1], [0, 0, 0, 0, -1, 0, -1, 0]]
        self.levels = self.get_levels()

    # Построение карты уровня по свойствам подземелья
    # Берем первое подземелье, строим его. При построении будет лестница вниз. В классе лестницы будет указатель на
    # карту, в которую она ведет. При указании этой карты создается новая и т.д. Так пробегутся все карты
    def self_get_levels(self):
        count_of_levels = len()

# Описание уровня: название, краткое название, тип карты уровня, уровень сложности, генерация карты уровня
class Levels:
    def __init__(self, name, short_name, difficalty = 0, map_type = 'rectangular', upstairs = [], downstairs = []):
        self.name = name
        self.short_name = short_name
        self.difficalty = difficalty
        self.map = Map_generator(map_type, upstairs, downstairs)