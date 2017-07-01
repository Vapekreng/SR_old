# На вход подаются координаты моба, его радиус видимости и логический массив 20 на 80, содержащий данные, какие клетки
# прозрачны, на выходе список координат клеток для отображения
#  TODO В данный момент не проверяются только уже проверенные клетки. Не проверять так же затемненные тайтлы и их окружение
diff = [[-1, 0], [0, -1], [0, 1], [1, 0]]
# diff = [[-1, 0], [0, -1], [0, 1], [1, 0], [1,1], [1,-1], [-1,-1], [-1,1]] Если сделать так, то получатся разрывы при
# взгляде через окна, поэтому оставил область видимости связной под 90 градусов


class AoS:
    def __init__(self, Hero, TestMap):
        self.walls = []
        self.aos = []
        self.checked = []
        self.transparent = TestMap.transparent_map
        self.vrange = Hero.sstats.range_of_visibility
        self.x = Hero.x
        self.y = Hero.y
        self.shadows = []
        for x in range(80):
            self.aos.append([False] * 20)
            self.checked.append([False] * 20)
            self.walls.append([False] * 20)
        for x in range(80):
            for y in range(20):
                if not self.transparent[x][y]:
                    self.walls[x][y] = [[True], [True], [True], [True], [True], [True], [True], [True]]

                # Выдает список координат видимых тайтлов

    def get(self):
        self.checked[self.x][self.y] = True
        self.aos[self.x][self.y] = True
        aos_list = []
        curr_list = [[self.x, self.y]]
        aos_list.append(curr_list[0])
        while curr_list:
            curr_list = self._get_next_list(curr_list)
            aos_list = aos_list + curr_list
        return aos_list

    def _can_see(self, x, y):
        x_new, y_new = new_coord(x, y, self.x, self.y)
        shadows = self.shadows
        visible = True
        if self.transparent[x][y]:
            for angles in shadows:
                if shaded(angles[0], angles[1], x_new, y_new):
                    visible = False
        else:
            corner = get_points_for_wall(x_new, y_new)
            walls=self.walls
            for angles in shadows:
                for i in range(8):
                    self.walls[x][y][i] = walls[x][y][i] and not shaded(angles[0], angles[1], corner[i][0],
                                                                             corner[i][1])
            visible = False
            for i in range(8):
                visible = visible or walls[x][y][i]
            if visible:
                self.shadows.append(get_shadow_angles(x, y, self.x, self.y))
        return visible

    def _get_next_list(self, curr_list):
        next_list = []
        x0=self.x
        y0=self.y
        vrange=self.vrange
        for t in curr_list:
            xc = t[0]
            yc = t[1]
            for d in diff:
                x = xc + d[0]
                y = yc + d[1]
                if in_vrange(x0, y0, x, y, vrange):
                    if in_map(x, y):
                        if not self.checked[x][y]:
                            self.checked[x][y] = True
                            if self._can_see(x, y):
                                next_list.append([x, y])
                                self.aos[x][y] = True
        return next_list

def in_vrange(x0, y0, x, y, vr):
    dist = (x0 - x) ** 2 + (y0 - y) ** 2
    if dist > vr ** 2:
        return False
    else:
        return True


def in_map(x, y):
    if -1 < x < 80 and -1 < y < 20:
        return True
    else:
        return False


def new_coord(x_old, y_old, x0, y0):
    x_new = 2 * (x_old - x0)
    y_new = 2 * (y_old - y0)
    return x_new, y_new


def get_points_for_wall(x, y):
    corner = [[x - 1, y], [x + 1, y], [x, y + 1], [x, y - 1], [x - 1, y + 1], [x + 1, y + 1], [x - 1, y - 1],
              [x + 1, y - 1]]
    return corner


def get_shadow_angles(x_old, y_old, x0, y0):
    x, y = new_coord(x_old, y_old, x0, y0)
    dx, dy = 1, 1
    if x < 0:
        dx = -1
    if y < 0:
        dy = -1
    x = abs(x)
    y = abs(y)
    if x * y > 0:
        angle1 = [x - 1, y + 1]
        angle2 = [x + 1, y - 1]
    elif x == 0:
        angle1 = [-1, y - 1]
        angle2 = [1, y - 1]
    else:
        angle1 = [x - 1, 1]
        angle2 = [x - 1, -1]
    angle1 = [dx * angle1[0], dy * angle1[1]]
    angle2 = [dx * angle2[0], dy * angle2[1]]
    return [angle1, angle2]


def shaded(angle1, angle2, xc_new, yc_new):
    is_shaded = False
    if angle1[0] * xc_new + angle1[1] * yc_new > 0 and angle2[0] * xc_new + angle2[1] * yc_new > 0:
        if (angle1[0] * yc_new - xc_new * angle1[1]) * (angle2[0] * yc_new - xc_new * angle2[1]) < 0:
            is_shaded = True
    return is_shaded
