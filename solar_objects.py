# coding: utf-8
# license: GPLv3

class SpaceBody:
    """Базовый класс для всех космических тел, содержащий физические параметры."""
    def __init__(self):
        self.m = 0
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.Fx = 0
        self.Fy = 0
        self.R = 5
        self.color = "red"
        self.image = None

    def move(self, dt):
        """Перемещает тело по методу Эйлера на основе действующих сил."""
        ax = self.Fx / self.m
        ay = self.Fy / self.m
        self.x += self.Vx * dt
        self.y += self.Vy * dt
        self.Vx += ax * dt
        self.Vy += ay * dt


class Star(SpaceBody):
    """Класс, описывающий звезду."""
    type = "star"


class Planet(SpaceBody):
    """Класс, описывающий планету."""
    type = "planet"

    def __init__(self):
        super().__init__()
        self.parent_star = None