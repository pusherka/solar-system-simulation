# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet


def read_space_objects_data_from_file(input_filename):
    """Считывает данные о космических объектах из файла, создаёт объекты.

    Параметры:
    **input_filename** — имя входного файла
    """
    objects = []
    current_star = None
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            parts = line.split()
            object_type = parts[0].lower()

            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
                current_star = star
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                planet.parent_star = current_star
                objects.append(planet)
            else:
                print(f"Unknown space object: {object_type}")

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Формат: Star <R> <цвет> <масса> <x> <y> <Vx> <Vy>
    """
    parts = line.split()
    star.R = int(parts[1])
    star.color = parts[2]
    star.m = float(parts[3])
    star.x = float(parts[4])
    star.y = float(parts[5])
    star.Vx = float(parts[6])
    star.Vy = float(parts[7])


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Формат: Planet <R> <цвет> <масса> <x> <y> <Vx> <Vy>
    """
    parts = line.split()
    planet.R = int(parts[1])
    planet.color = parts[2]
    planet.m = float(parts[3])
    planet.x = float(parts[4])
    planet.y = float(parts[5])
    planet.Vx = float(parts[6])
    planet.Vy = float(parts[7])


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.

    Параметры:
    **output_filename** — имя выходного файла
    **space_objects** — список сохраняемых объектов
    """
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        for obj in space_objects:
            out_file.write(
                f"{obj.type.capitalize()} {obj.R} {obj.color} {obj.m} "
                f"{obj.x} {obj.y} {obj.Vx} {obj.Vy}\n"
            )


if __name__ == "__main__":
    print("This module is not for direct call!")