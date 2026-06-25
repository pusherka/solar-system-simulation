# coding: utf-8
# license: GPLv3

import math

# Безопасное расстояние сближения между планетами разных звёзд (в метрах)
MIN_DISTANCE = 1.5E10


def _too_close(planet, all_objects):
    """
    Проверяет, не подошла ли планета слишком близко к планетам других звёзд.
    """
    for other in all_objects:
        if other is planet or other.type != "planet":
            continue

        # Нам интересны только столкновения между планетами РАЗНЫХ звезд
        parent_self = getattr(planet, 'parent_star', None)
        parent_other = getattr(other, 'parent_star', None)
        if parent_self is not None and parent_other is not None and parent_self is parent_other:
            continue

        # Считаем расстояние между ними
        dist = math.hypot(planet.x - other.x, planet.y - other.y)
        if dist < MIN_DISTANCE:
            return True
    return False


def recalculate_space_objects_positions(space_objects, dt):
    """
    Кинематический расчет координат:
    1. Звёзды вращаются вокруг общего центра масс (если у них задана ненулевая скорость),
       иначе они остаются абсолютно статичными.
    2. Планеты вращаются вокруг своих parent_star с учетом движения самих звёзд.
       Предусмотрено предотвращение столкновений планет разных звёзд.
    """
    stars = [obj for obj in space_objects if obj.type == "star"]

    # 1. Находим общий центр масс звезд (для двойной звезды это будет точка (0, 0))
    total_star_mass = sum(star.m for star in stars)
    if total_star_mass > 0:
        bary_cx = sum(star.x * star.m for star in stars) / total_star_mass
        bary_cy = sum(star.y * star.m for star in stars) / total_star_mass
    else:
        bary_cx, bary_cy = 0.0, 0.0

    # 2. Инициализируем параметры движения звезд и планет (при первом шаге)
    for body in space_objects:
        if body.type == "star":
            if not hasattr(body, 'orbit_r'):
                dx = body.x - bary_cx
                dy = body.y - bary_cy
                body.orbit_r = math.hypot(dx, dy)
                body.angle = math.atan2(dy, dx)
                body.cx = bary_cx
                body.cy = bary_cy

                # Если у звезды на старте есть скорость, рассчитываем угловую скорость вращения
                if body.orbit_r > 0 and (body.Vx != 0 or body.Vy != 0):
                    cross_product = dx * body.Vy - dy * body.Vx
                    body.omega = cross_product / (body.orbit_r ** 2)
                else:
                    body.omega = 0.0

        elif body.type == "planet" and getattr(body, 'parent_star', None) is not None:
            star = body.parent_star
            if not hasattr(body, 'orbit_r'):
                dx = body.x - star.x
                dy = body.y - star.y
                body.orbit_r = math.hypot(dx, dy)
                body.angle = math.atan2(dy, dx)

                if body.orbit_r > 0:
                    cross_product = dx * body.Vy - dy * body.Vx
                    body.omega = cross_product / (body.orbit_r ** 2)
                else:
                    body.omega = 0.0

    # 3. Движение звезд вокруг барицентра
    for star in stars:
        if getattr(star, 'omega', 0.0) != 0.0:
            star.angle += star.omega * dt
            star.x = star.cx + star.orbit_r * math.cos(star.angle)
            star.y = star.cy + star.orbit_r * math.sin(star.angle)

        # Обнуляем физику для корректной работы move()
        star.Vx = 0
        star.Vy = 0
        star.Fx = 0
        star.Fy = 0

    # 4. Движение планет вокруг (возможно, движущихся) звезд
    for body in space_objects:
        if body.type == "planet" and getattr(body, 'parent_star', None) is not None:
            star = body.parent_star

            # Рассчитываем положение относительно нового (сдвинутого) положения звезды
            next_angle = body.angle + body.omega * dt
            next_x = star.x + body.orbit_r * math.cos(next_angle)
            next_y = star.y + body.orbit_r * math.sin(next_angle)

            # Временно сохраняем координаты
            old_x, old_y = body.x, body.y
            body.x, body.y = next_x, next_y

            # Если сближение с чужой планетой слишком опасное — откатываемся
            if _too_close(body, space_objects):
                body.x, body.y = old_x, old_y
            else:
                body.angle = next_angle

            # Сбрасываем линейные скорости
            body.Vx = 0
            body.Vy = 0
            body.Fx = 0
            body.Fy = 0

    # 5. Вызываем move() для очистки вызовов
    for body in space_objects:
        body.move(dt)