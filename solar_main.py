# coding: utf-8
# license: GPLv3

import os
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from solar_vis import *
from solar_model import *
from solar_input import *

DEFAULT_SYSTEM_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticket_2_system.txt")

perform_execution = False
physical_time = 0
displayed_time = None
time_step = None
space_objects = []
show_orbits = False
orbit_lines = []


def execution():
    global physical_time, displayed_time

    try:
        dt = time_step.get()
    except tkinter.TclError:
        dt = 100000.0

    recalculate_space_objects_positions(space_objects, dt)

    for body in space_objects:
        update_object_position(space, body, show_orbits)

    physical_time += dt
    displayed_time.set("%.1f s" % physical_time)

    if perform_execution:
        space.after(max(1, 101 - int(time_speed.get())), execution)


def start_execution():
    global perform_execution, start_button
    if not space_objects:
        return
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution
    execution()


def stop_execution():
    global perform_execution, start_button
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution


def clear_orbits():
    global orbit_lines
    for line in orbit_lines:
        space.delete(line)
    orbit_lines.clear()


def build_orbits():
    global orbit_lines, space_objects
    clear_orbits()
    stars = [obj for obj in space_objects if obj.type == "star"]
    planets = [obj for obj in space_objects if obj.type == "planet"]

    # 1. Строим орбиты планет вокруг их родительских звёзд
    for planet in planets:
        parent_star = planet.parent_star
        if parent_star is None and stars:
            parent_star = min(stars, key=lambda s: (s.x - planet.x) ** 2 + (s.y - planet.y) ** 2)
        if parent_star is not None:
            line = draw_static_orbit(space, parent_star, planet)
            orbit_lines.append(line)

    # 2. Строим орбиты звезд вокруг центра масс, ТОЛЬКО если они реально движутся (двойная звезда)
    if len(stars) >= 2:
        # Проверяем, задана ли хоть какой-то звезде начальная скорость
        any_star_moving = any(star.Vx != 0 or star.Vy != 0 for star in stars)
        if any_star_moving:
            total_mass = sum(star.m for star in stars)
            if total_mass > 0:
                cx = sum(star.x * star.m for star in stars) / total_mass
                cy = sum(star.y * star.m for star in stars) / total_mass
                for star in stars:
                    line = draw_barycentric_orbit(space, star, cx, cy)
                    orbit_lines.append(line)


def load_system_from_file(in_filename):
    global space_objects, physical_time
    stop_execution()
    for obj in space_objects:
        space.delete(obj.image)
    clear_orbits()

    space_objects = read_space_objects_data_from_file(in_filename)
    if not space_objects:
        return

    calculate_scale_factor(space_objects)

    for obj in space_objects:
        if obj.type == "star":
            create_star_image(space, obj)
        elif obj.type == "planet":
            create_planet_image(space, obj)

    if show_orbits:
        build_orbits()

    physical_time = 0
    displayed_time.set("0.0 s")


def open_file_dialog():
    in_filename = askopenfilename(
        initialdir=os.path.dirname(DEFAULT_SYSTEM_FILE),
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if in_filename:
        load_system_from_file(in_filename)


def save_file_dialog():
    if not space_objects:
        return
    out_filename = asksaveasfilename(
        initialdir=os.path.dirname(DEFAULT_SYSTEM_FILE),
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if not out_filename:
        return
    write_space_objects_data_to_file(out_filename, space_objects)


def main():
    global physical_time, displayed_time, time_step, time_speed
    global space, start_button, orbit_button

    root = tkinter.Tk()
    root.title("Solar System — Ticket 2")
    root.resizable(False, False)

    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)

    frame = tkinter.Frame(root, padx=6, pady=6)
    frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=7)
    start_button.pack(side=tkinter.LEFT, padx=(0, 4))

    tkinter.Label(frame, text="dt:").pack(side=tkinter.LEFT)
    time_step = tkinter.DoubleVar(value=100000.0)
    tkinter.Entry(frame, textvariable=time_step, width=10).pack(side=tkinter.LEFT, padx=(2, 8))

    time_speed = tkinter.DoubleVar(value=100)
    tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL, label="Speed", length=120).pack(
        side=tkinter.LEFT, padx=(0, 8)
    )

    tkinter.Button(frame, text="Open file...", command=open_file_dialog).pack(side=tkinter.LEFT, padx=2)
    tkinter.Button(frame, text="Save to file...", command=save_file_dialog).pack(side=tkinter.LEFT, padx=2)

    def toggle_orbits():
        global show_orbits
        show_orbits = not show_orbits
        if show_orbits:
            orbit_button['text'] = "Orbits: ON"
            build_orbits()
        else:
            orbit_button['text'] = "Orbits: OFF"
            clear_orbits()

    orbit_button = tkinter.Button(frame, text="Orbits: OFF", command=toggle_orbits)
    orbit_button.pack(side=tkinter.LEFT, padx=(8, 4))

    displayed_time = tkinter.StringVar(value="0.0 s")
    tkinter.Label(frame, textvariable=displayed_time, width=12, anchor="w").pack(side=tkinter.LEFT)

    root.mainloop()


if __name__ == "__main__":
    main()
