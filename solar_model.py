# coding: utf-8
# license: GPLv3

import math


def recalculate_space_objects_positions(space_objects, dt):
    """
    Кинематическая модель движения:
    Планеты двигаются по идеальным кругам с помощью тригонометрии (без гравитации).
    """
    for body in space_objects:
        if body.type == "planet" and getattr(body, 'parent_star', None) is not None:
            star = body.parent_star

            # Если планета только что загрузилась, динамически вычисляем её параметры
            if not hasattr(body, 'angle'):
                dx = body.x - star.x
                dy = body.y - star.y

                # Фиксируем радиус орбиты
                body.orbit_r = math.hypot(dx, dy)

                # Фиксируем начальный угол положения
                body.angle = math.atan2(dy, dx)

                # Вычисляем угловую скорость (радианы в секунду).
                # Векторное произведение позволяет определить, куда должна крутиться планета
                # (по часовой или против) исходя из начальных скоростей Vx и Vy из твоего файла.
                cross_product = dx * body.Vy - dy * body.Vx
                body.omega = cross_product / (body.orbit_r ** 2)

            # Шаг 1: Изменяем угол на основе времени и угловой скорости
            body.angle += body.omega * dt

            # Шаг 2: Вычисляем новые идеальные координаты через синус и косинус
            body.x = star.x + body.orbit_r * math.cos(body.angle)
            body.y = star.y + body.orbit_r * math.sin(body.angle)

            # Обнуляем обычную физическую скорость и силы, чтобы старый метод .move()
            # из solar_objects.py ничего не искажал.
            body.Vx = 0
            body.Vy = 0
            body.Fx = 0
            body.Fy = 0

    # Для обратной совместимости с базовой архитектурой вызываем move(),
    # но так как скорости и силы равны 0, он просто пропустит физику.
    for body in space_objects:
        body.move(dt)