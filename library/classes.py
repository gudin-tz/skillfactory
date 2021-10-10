import random
from tkinter import *


class FleetCreating:

    def __init__(self, pad_side):
        self.basic = 6
        self.fleet = [4, 2, 1]
        self.pad = []
        self.fleet_position = []
        self.ships_in_fleet = 0

        for i in range(pad_side):
            for j in range(pad_side):
                self.pad.append([i, j])

        for i in range(len(self.fleet)):
            ships_by_mast = self.fleet[i] + self.fleet[i] * (pad_side - self.basic)
            self.ships_in_fleet += ships_by_mast
            for ship in range(ships_by_mast):
                attempt = 0
                while not self.ship_placement(i + 1) and attempt < 10000:
                    attempt += 1

    def ship_placement(self, nom):

        def side_check():
            if position[1] + nom > self.basic:
                return False
            return True

        def space_pad_check():
            result = True
            delta = []
            if nom > 0:
                if direction == 0:
                    for i in range(nom):
                        position_check = [position[0], position[1] + i]
                        result = result * (position_check in self.pad)
                        delta.append(position_check)
                        delta.append([position[0] + 1, position[1]])
                        delta.append([position[0] - 1, position[1]])
                        if i == 0:
                            delta.append([position[0], position[1] - 1])
                        elif i == nom:
                            delta.append([position[0], position[1] + 1])
                    if result:
                        self.fleet_position.append([direction, nom, position])
                        for el in delta:
                            if el in self.pad:
                                self.pad.remove(el)
                        return True
                if direction == 1:
                    for i in range(nom):
                        position_check = [position[0] + i, position[1]]
                        result = result * (position_check in self.pad)
                        delta.append(position_check)
                        delta.append([position[0], position[1] + 1])
                        delta.append([position[0], position[1] - 1])
                        if i == 0:
                            delta.append([position[0] - 1, position[1]])
                        elif i == nom:
                            delta.append([position[0] + 1, position[1]])
                    if result:
                        self.fleet_position.append([direction, nom, position])
                        for el in delta:
                            if el in self.pad:
                                self.pad.remove(el)
                        return True
            else:
                self.fleet_position.append([direction, nom, position])
                self.pad.remove(position)
                return True

            return False

        direction = random.randint(0, 1)
        position = random.choice(self.pad)

        if side_check():
            if space_pad_check():
                return [self.ships_in_fleet, self.fleet_position]

        return False


class GamePad:

    def __init__(self, gamer, pad_side, fleet_position):
        self.pad = Tk()
        self.gamer = gamer
        self.pad.side = pad_side
        self.pad.cells = []
        self.buttons = []
        self.active = None
        self.fleet_position = fleet_position

    def create_pad(self):
        def cell_press(a, b):
            self.buttons[a * self.pad.side + b].destroy()

        def set_ship():
            for ship in self.fleet_position:
                if ship[0] == 0:
                    for x in range(ship[1]):
                        lbl = Label(text=ship[1], bg='red', relief="groove")
                        lbl.grid(row=ship[2][0], column=ship[2][1] + x, sticky='nwse')
                else:
                    for x in range(ship[1]):
                        lbl = Label(text=ship[1], bg='red', relief="groove")
                        lbl.grid(row=ship[2][0] + x, column=ship[2][1], sticky='nwse')

        for i in range(self.pad.side):
            for j in range(self.pad.side):
                self.pad.rowconfigure(i, minsize=30)
                self.pad.columnconfigure(j, minsize=30)
                Label(width=2).grid(row=i, column=j)

        set_ship()

        for i in range(self.pad.side):
            for j in range(self.pad.side):
                if self.gamer == 'human':
                    button = Button(relief="groove", command=lambda a=i, b=j: cell_press(a, b))
                    button.grid(row=i, column=j)
                    self.buttons.append(button)
                self.pad.cells.append((str(i) + ',' + str(j)))