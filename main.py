import time
from tkinter import *
from tkinter import messagebox
import random

tk = Tk()
app_running = True

size_canvas_x = 400
size_canvas_y = 400
s_x = s_y = 10  # Field size
step_x = size_canvas_x // s_x
step_y = size_canvas_y // s_y
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y

menu_x = step_x * 4 #250

ships = s_x // 2
ship_len1 = s_x // 5
ship_len2 = s_x // 3
ship_len3 = s_x // 2
enemy_ships = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]
list_ids = []
points = [[-1 for i in range(s_x)] for i in range(s_y)]

boom = [[0 for i in range(s_x)] for i in range(s_y)]


def on_closing():
    global app_running
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        app_running = False
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("See Battle")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)  # TODO Delete after ending project
canvas = Canvas(tk, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + 10, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y,
                        fill="lightyellow")
canvas.pack()
tk.update()


def draw_table(offset_x=0):
    for i in range(0, s_x + 1):
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)


draw_table()
draw_table(size_canvas_x + menu_x)


def button_show_enemy():
    show_enemy()


def show_enemy():
    global points
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:
                color = "red"
                if points[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)
    points = [[0 for i in range(s_x)] for i in range(s_y)]


def button_restart():
    global list_ids
    global points
    global boom
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_enemy_ships()
    points = [[-1 for i in range(s_x)] for i in range(s_y)]
    boom = [[0 for i in range(s_x)] for i in range(s_y)]


b0 = Button(tk, text="Show enemy ship", command=button_show_enemy)
b0.place(x=size_canvas_x + 20, y=30)
b1 = Button(tk, text="Restart", command=button_restart)
b1.place(x=size_canvas_x + 20, y=70)


def draw_point(x, y):
    if enemy_ships[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(x * step_x+step_x//3, y * step_y+step_y//3, x * step_x + step_x - step_x//3, y * step_y + step_y - step_y//3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    else :
        color="blue"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def check_winner(x, y):
    win = False
    if enemy_ships[y][x] > 0:
        boom[y][x] = enemy_ships[y][x]
    sum_enemy_ships = sum(sum(i) for i in zip(*enemy_ships))
    sum_boom = sum(sum(i) for i in zip(*boom))
    if sum_enemy_ships == sum_boom:
        win = True
    return win


def add_to_all(event):
    global points
    _type = 0
    if event.num == 3:
        _type = 1
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_X = mouse_x // step_x
    ip_Y = mouse_y // step_y
    # print(ip_X, ip_y, "_type", _type)
    if ip_X < s_x and ip_Y < s_y:
        if points[ip_Y][ip_X] == -1:
            points[ip_Y][ip_X] = _type
            draw_point(ip_X, ip_Y)
            if check_winner(ip_X, ip_Y):
                print("!!!WINNER!!!")
                points = [[0 for i in range(s_x)] for i in range(s_y)]
                show_enemy()



canvas.bind_all("<Button-1>", add_to_all)
canvas.bind_all("<Button-3>", add_to_all)


def generate_enemy_ships():
    global enemy_ships
    ships_list = []
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))
    # print(ships_list)

    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0

    while sum_1_enemy != sum_1_all_ships:
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(s_x + 1)] for i in
                       range(s_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное

            primerno_x = random.randrange(0, s_x)
            if primerno_x + len > s_x:
                primerno_x = primerno_x - len

            primerno_y = random.randrange(0, s_y)
            if primerno_y + len > s_y:
                primerno_y = primerno_y - len

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1:
                if primerno_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1

        # print(sum_1_enemy)
        # print(ships_list)
        # print(enemy_ships)


generate_enemy_ships()

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
