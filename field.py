import tkinter as tk


class Field:
    def __init__(self, parent):
        self.field = tk.Canvas(parent, width=500, height=800, bg="green")
        self.field.grid(row=0, column=1, rowspan=3, padx=10, pady=10)

        self.positions = []

        for i in range(12):
            self.set_positions(self.get_coords(i))

        self.field.create_line(0, 400, 500, 400, width=10, fill="white")
        self.field.create_rectangle(100, -10, 400, 90, width=10, outline="white")
        self.field.create_rectangle(100, 710, 400, 810, width=10, outline="white")

    def set_positions(self, coords):
        x, y = coords
        position = self.field.create_text(x, y, font="Default 14")
        self.positions.append(position)

    def get_coords(self, i):
        x, y = (0, 0)

        if i == 0:
            x, y = (250, 50)
        elif i == 1:
            x, y = (150, 150)
        elif i == 2:
            x, y = (350, 150)
        elif i == 3:
            x, y = (250, 250)
        elif i == 4:
            x, y = (250, 350)
        elif i == 5:
            x, y = (250, 750)
        elif i == 6:
            x, y = (150, 650)
        elif i == 7:
            x, y = (350, 650)
        elif i == 8:
            x, y = (250, 550)
        elif i == 9:
            x, y = (250, 450)

        return (x, y)

    def players(self, players, colors):
        for i, player in enumerate(players):
            name = player.name.split(" ")
            name = name[0][0] + ". " + " ".join(name[1:])
            self.field.insert(i + 1, tk.END, name)

            color = ""
            if i < 5:
                color = colors[0]
            else:
                color = colors[1]

            self.field.itemconfig(i + 1, fill=color)
