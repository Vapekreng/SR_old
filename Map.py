import AreaOfSight, Config, random
from bearlibterminal import terminal

# Ширина экрана
screen_width = Config.screen_width

# Высота экрана
screen_height = Config.screen_height

# Прописываем свойства рельефа: иконка, прозрачность, проходимость, цвет. Проходимость показывает изменение базовой
# стоимости передвижения по данной ячейке: 100 - обычная скорость, 50 - половинная, 0 - непроходимая пешком ячейка

relief_floor = {'icon': '.', 'transparent': True, 'passable': 100, 'color': 'white', 'move speed': 100}
relief_wall = {'icon': '#', 'transparent': False, 'passable': 0, 'color': 'white', 'move speed': 100}
relief_grass = {'icon': '.', 'transparent': True, 'passable': 80, 'color': 'green', 'move speed': 100}

reliefs = {'floor': relief_floor, 'wall': relief_wall, 'grass': relief_grass,}

# В ячейке карты могут быть объекты 4 видов: рельеф, мобы, предметы, эффекты. Класс Title собирает их вместе

class Title:
    def __init__(self, x, y, relief_type = 'floor'):
        self.relief = relief(relief_type)
        self.mob = None
        self.items = []
        self.effects = []

# Класс - прародитель объектов карты, сюда буду выносить общие черты объектов карты

# class Map_object:

# Рельеф - пол, стены, трава, дорога, вода - постоянные объекты, которые не могут передвигаться. Изменяются под
# внешним воздействием

class Relief:
    def __init__(self, name):
        self.name = name
        self.icon = reliefs[name]['icon']
        self.transparent = reliefs[name]['transparent']
        self.passable = reliefs[name]['passable']
        self.color = reliefs[name]['color']
        self.base_speed_cost = reliefs[name]['move speed']

# Моб - объект, способный на самостоятельные действия, такие, как атака, передвижение, колдовство, разговор

# Предмет - объект, который можно поместить в рюкзак

# Эффекты - объекты, которые могут оказывать воздействие на рельеф, моба или карту целиком, исчезают со временем -
# туман, отравление, ветер, жара, холод


# Комната - свободное пространство в виде прямоугольника. Изначально комната занимает всю карту, кроме границ - там
# стены, поэтому у высоты и ширины отнимается по 2

class Rooms:
    def __init__(self, x0 = 1, y0 = 1, x1 = screen_width - 2, y1 = screen_height - 2):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.dx = x1-x0
        self.dy = y1 - y0
        self.area = self.dx * self.dy

    # Минимальная ширина комнаты у меня 3, поэтому комнаты делятся только если размерность 7 или больше. Делится по
    # большей размерности

    def separate(self):
        if self.dx > self.dy

class Maps:
    def __init__(self, name: str = 'TestMap', width = screen_width, height = screen_height - 5):
        self.name = name
        self.width = width
        self.height = height
        self.mobs_counter = 0
        self.mob_list = []
        self.title = []
        self.icon_buffer = []
        self.icon_map = []
        self.transparent_map=[]
        for x in range(80):
            self.title.append([1] * 20)
            self.icon_buffer.append(['!!!'] * 20)
            self.icon_map.append([' ']*20)
            self.transparent_map.append([True]*20)
        for x in range(80):
            for y in range(20):
                self.title[x][y] = Titles(x, y)
                if (x * y * (x - 79) * (y - 19) == 0) or (x % 10 == 0 and y % 10 != 0):
                    self.title[x][y].relief = Relief('wall')
        for x in range(80):
            for y in range(20):
                self.icon_map[x][y] = self.get_title_char(x, y)
                if not self.title[x][y].relief.transparent:
                    self.transparent_map[x][y]=False

    def get_title_char(self, x, y):
        title = self.title[x][y]
        char = title.relief.icon
        if title.mob:
            char = title.mob.icon
        else:
            if title.items:
                char = '!'
        return char

    def draw(self, aos_list):
        icon_map=self.icon_map
        icon_on_screen=self.icon_on_screen
        for t in aos_list:
            x = t[0]
            y = t[1]
            icon = icon_map[x][y]
            if icon_on_screen[x][y] != icon:
                terminal.printf(x, y + 2, icon)
                self.icon_on_screen[x][y] = icon

    def add_mob(self, mob):
        self.mob_list = self.mob_list.append(mob)
        self.title[mob.x][mob.y].mob = mob
        self.mobs_counter += 1
        self.icon_map[mob.x][mob.y]=self.get_title_char(mob.x,mob.y)

    def move_mob(self, mob, key):
        """

        :param mob: Mobs
        :type time: int
        """
        dx = 0
        dy = 0
        if key == Config.comand['left'] or key == Config.comand['arrow left']:
            dx = -1
            dy = 0
        if key == Config.comand['right'] or key == Config.comand['arrow right']:
            dx = 1
            dy = 0
        if key == Config.comand['up'] or key == Config.comand['arrow up']:
            dx = 0
            dy = -1
        if key == Config.comand['down'] or key == Config.comand['arrow down']:
            dx = 0
            dy = 1
        x = mob.x + dx
        y = mob.y + dy
        passable = self.title[x][y].mob is None and self.title[x][y].relief.passable
        if passable:
            self.title[mob.x][mob.y].mob = None
            self.icon_map[mob.x][mob.y] = self.get_title_char(mob.x, mob.y)
            mob.x += dx
            mob.y += dy
            self.title[mob.x][mob.y].mob = mob
            self.icon_map[mob.x][mob.y] = self.get_title_char(mob.x, mob.y)
            # TODO возвращать потраченное количество энергии
            return 1
        else:
            return 0

class PrimaryStats:
    def __init__(self, strength=0, toughness=0, dexterity=0, wisdom=0, perception=0, intelligence=0):
        """

        :type intelligence: int
        """
        self.strength = strength
        self.toughness = toughness
        self.dexterity = dexterity
        self.wisdom = wisdom
        self.perception = perception
        self.intelligence = intelligence


class SecondaryStats:
    def __init__(self, pstats):
        """

        :type pstats: PrimaryStats
        """
        self.range_of_visibility = 5 + pstats.perception


class Mobs:
    def __init__(self, x: int, y: int, mob_id: int, name: str, icon: chr, race: str):
        """

        :type x: int
        :type y: int
        :type mob_id: int
        :type name: str
        :type icon: char
        """
        self.id = mob_id
        self.name = name
        self.icon = icon
        self.x = x
        self.y = y
        self.pstats = PrimaryStats()
        self.sstats = SecondaryStats(self.pstats)
        self.race = race
        self.aos = []

# Рельеф - все то, что не может двигаться или быть перемещено
# Свойства рельефа


# И собираем их все в общий словарь, чтобы потом использовать при создании экземпляров
propeties = {'floor': floor_propeties, 'wall': wall_propeties}


# TODO: перекинуть все свойства тайтлов в файлы

class Relief:
    def __init__(self, name: str):
        self.icon = propeties[name]['icon']
        self.transparent = propeties[name]['transparent']
        self.passable = propeties[name]['passable']
        self.color = propeties[name]['color']


# Тайтл это минимальное место, на котором могут располагается игровые элементы: мобы, предметы и т.д.
# +2 в игрике - оставляем 2 строки сверху для текста
class Titles:
    def __init__(self, x, y):
        self.relief = Relief('floor')
        self.mob = None
        self.items = []
        self.x = x
        self.y = y

        # TODO добавить проверку предметов на земле




    # TODO: add_mob проверка, что не занято, добавка параметров расы, уровня опасности подземелья, враждебности


def run_game():
    terminal.clear()
    TestMap = Maps()
    Hero = Mobs(19, 10, 0, '455', '@', 'human')
    # TODO: Перекинуть добавку моба в класс мобов
    TestMap.add_mob(Hero)
    aos = AreaOfSight.AoS(Hero, TestMap)
    TestMap.draw(aos.get())
    time = 0
    terminal.printf(0, 0, 'time=' + str(time))
    terminal.refresh()
    # TODO: Обработчик нажатий клавиш, мэйн луп, настройка клавиатуры через меню
    while True:
        key = terminal.read()
        while key not in Config.comand.values():
            key=terminal.read()
        if key == Config.comand['close'] or key == Config.comand['esc']:
            break
        time+=TestMap.move_mob(Hero, key)
        aos = AreaOfSight.AoS(Hero, TestMap)
        TestMap.draw(aos.get())
        terminal.printf(0, 0, 'time=' + str(time))
        terminal.refresh()
    terminal.clear()
    terminal.refresh()