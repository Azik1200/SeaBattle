import time
from tkinter import *
from tkinter import messagebox

tk = Tk()
app_running = True

size_canvas_x = 600
size_canvas_y = 600
s_x = s_y = 10  # Field size
step_x = size_canvas_x // s_x
step_y = size_canvas_y // s_y
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y

menu_x = 250

ships = s_x // 2
ship_len1 = s_x // 5
ship_len2 = s_x // 3
ship_len3 = s_x // 2
enemy_ships = [[0 for i in range(s_x)] for i in range(s_y)]


def on_closing():
    global app_running
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        app_running = False
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("See Battle")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)  # TODO Delete after ending project
canvas = Canvas(tk, width=size_canvas_x + menu_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.pack()
tk.update()


def draw_table():
    for i in range(0, s_x + 1):
        canvas.create_line(step_x * i, 0, step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(0, step_y * i, size_canvas_x, step_y * i)


draw_table()


def button_show_enemy():
    pass


def button_restart():
    pass


b0 = Button(tk, text="Show enemy ship", command=button_show_enemy)
b0.place(x=size_canvas_x + 20, y=30)
b1 = Button(tk, text="Restart", command=button_restart)
b1.place(x=size_canvas_x + 20, y=70)


def add_to_all(event):
    _type = 0
    if event.num == 3:
        _type = 1
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_X = mouse_x // step_x
    ip_y = mouse_y // step_y
    # print(ip_X, ip_y, "_type", _type)


canvas.bind_all("<Button-1>", add_to_all)
canvas.bind_all("<Button-3>", add_to_all)


def generate_enemy_ships():
    global enemy_ships


generate_enemy_ships()

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
