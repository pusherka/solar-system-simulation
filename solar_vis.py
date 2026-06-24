# coding: utf-8
# license: GPLv3

import math

window_width = 800
window_height = 800
scale_factor = None
center_x = 0
center_y = 0
canvas_margin = 25


def calculate_scale_factor(space_objects):
    """Подбирает масштаб и смещение, чтобы все тела и орбиты влезли в окно."""
    global scale_factor, center_x, center_y

    if not space_objects:
        scale_factor = 1
        center_x = 0
        center_y = 0
        return

    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    for obj in space_objects:
        min_x = min(min_x, obj.x)
        max_x = max(max_x, obj.x)
        min_y = min(min_y, obj.y)
        max_y = max(max_y, obj.y)

    for obj in space_objects:
        if obj.type != "planet" or obj.parent_star is None:
            continue
        star = obj.parent_star
        orbit_r = math.hypot(obj.x - star.x, obj.y - star.y)
        min_x = min(min_x, star.x - orbit_r)
        max_x = max(max_x, star.x + orbit_r)
        min_y = min(min_y, star.y - orbit_r)
        max_y = max(max_y, star.y + orbit_r)

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max(max_x - min_x, 1)
    height = max(max_y - min_y, 1)

    scale_factor = 0.92 * min(
        (window_width - 2 * canvas_margin) / width,
        (window_height - 2 * canvas_margin) / height
    )
    print('Scale factor:', scale_factor)


def scale_x(x):
    return int((x - center_x) * scale_factor) + window_width // 2


def scale_y(y):
    return window_height // 2 - int((y - center_y) * scale_factor)


def create_star_image(space, star):
    x = scale_x(star.x)
    y = scale_y(star.y)
    r = star.R
    star.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=star.color)


def create_planet_image(space, planet):
    x = scale_x(planet.x)
    y = scale_y(planet.y)
    r = planet.R
    planet.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=planet.color)


def draw_static_orbit(space, star, planet):
    """Рисует круговую орбиту планеты вокруг её звезды."""
    dx = planet.x - star.x
    dy = planet.y - star.y
    r_physics = (dx ** 2 + dy ** 2) ** 0.5
    r_pixels = int(r_physics * scale_factor)

    cx = scale_x(star.x)
    cy = scale_y(star.y)

    orbit_id = space.create_oval(
        cx - r_pixels, cy - r_pixels,
        cx + r_pixels, cy + r_pixels,
        outline="#666666",
        dash=(2, 4),
        width=1
    )
    space.tag_lower(orbit_id)
    return orbit_id


def update_object_position(space, body, show_orbits=False):
    """Обновляет позицию объекта на экране."""
    x = scale_x(body.x)
    y = scale_y(body.y)
    r = body.R
    space.coords(body.image, x - r, y - r, x + r, y + r)
    return None
