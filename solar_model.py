# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11


def calculate_force(body, space_objects):
    """Вычисляет проекции сил притяжения, действующих на тело со стороны всех остальных объектов."""
    body.Fx = 0
    body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue
        dx = obj.x - body.x
        dy = obj.y - body.y
        r = (dx ** 2 + dy ** 2) ** 0.5

        if r < 1:
            continue

        f = gravitational_constant * body.m * obj.m / (r ** 2)
        body.Fx += f * (dx / r)
        body.Fy += f * (dy / r)


def recalculate_space_objects_positions(space_objects, dt):
    """Управляет силами и заставляет объекты сделать шаг перемещения в парадигме ООП."""
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        body.move(dt)