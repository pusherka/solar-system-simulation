# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11


def calculate_force(body, space_objects):
    """Вычисляет проекции сил притяжения, действующих на тело.
    Если у планеты есть parent_star, она притягивается строго к ней.
    """
    body.Fx = 0
    body.Fy = 0

    if body.type == "planet" and getattr(body, 'parent_star', None) is not None:
        # Планета притягивается ТОЛЬКО к своей родительской звезде, заданной при парсинге
        star = body.parent_star
        dx = star.x - body.x
        dy = star.y - body.y
        r = (dx ** 2 + dy ** 2) ** 0.5

        if r >= 1:
            f = gravitational_constant * body.m * star.m / (r ** 2)
            body.Fx += f * (dx / r)
            body.Fy += f * (dy / r)

    else:
        # Для звёзд сохраняем стандартное взаимное притяжение (если звёзд несколько)
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