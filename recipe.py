import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet

bg_colour = "#734f96"

shanti = pyglet.font.add_file("fonts\\shanti.ttf")
ubuntu = pyglet.font.add_file("fonts\\ubuntu.ttf")


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    connection = sqlite3.connect("data\\recipes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()
    index = random.randint(0, len(all_tables)-1)

    #fetch ingredients 
    table_name =  all_tables[index][1]
    cursor.execute("SELECT * FROM "+ table_name +";")
    table_records = cursor.fetchall()

    connection.close()
    return table_name, table_records

def pre_process(table_name, table_records):
    title = table_name[:-6]
    title = "".join([char if char.islower() else " "+ char for char in title])
    print(title)


    ingredients = []
    #for ingredients 
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " " + "of " + name)

    return title, ingredients


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    global logo_img
    frame1.pack_propagate(False)
    
    #load the recipes logo
    logo_img = ImageTk.PhotoImage(file="Images\\Recipeboxfinal.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg = bg_colour)
    logo_widget_image = logo_img
    logo_widget.pack()

    tk.Label(
        frame1,
        text = "Are you ready to try a new recipe today?",
        bg = bg_colour,
        fg = "white",
        font = (shanti, 14)
    ).pack()

#button
    tk.Button(
        frame1,
        text = "SHUFFLE",
        font = (ubuntu, 20),
        bg = "#E6E6FA",
        fg = "#306433",
        cursor = "hand2",
        activebackground = "#99EDC3",
        activeforeground = "black",
        command = lambda:load_frame2()).pack(pady = 20)

def load_frame2():

    clear_widgets(frame1)
    global logo_img
    frame2.tkraise()
    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)

    logo_img = ImageTk.PhotoImage(file="Images\Recipemodified.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg = bg_colour)
    logo_widget_image = logo_img
    logo_widget.pack(pady = 20)

    tk.Label(
        frame2,
        text = title,
        bg = bg_colour,
        fg = "white",
        font = (ubuntu, 20)
        ).pack(pady = 25)

    for i in ingredients:
        tk.Label(
            frame2,
            text = i,
            bg = "#E6E6FA",
            fg = "black",
            font = (shanti, 12)
            ).pack(fill = "both")

    tk.Button(
        frame2,
        text = "BACK",
        font = (ubuntu, 18),
        bg = "#E6E6FA",
        fg = "#306433",
        cursor = "hand2",
        activebackground = "#99EDC3",
        activeforeground = "black",
        command = lambda:load_frame1()).pack(pady = 20)


#initialize
root = tk.Tk()
#title of the window
root.title("Recipe Picker")
#alignment of window
root.eval("tk::PlaceWindow . center")


frame1 = tk.Frame(root, width = 500, height = 600, bg = bg_colour)
frame2 = tk.Frame(root, bg = bg_colour)

for frame in (frame1, frame2):
    frame.grid(row = 0, column = 0, sticky = "nesw")

load_frame1()

root.mainloop()