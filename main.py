#!/usr/bin/python3

from library import classes
import sys

if __name__ == '__main__':

    side = 6
    fleets = {}

    for gamer in ['human', 'ai']:
        value = classes.FleetCreating(side)
        if len(value.fleet_position) == value.ships_in_fleet:
            game_pad = classes.GamePad(gamer, side, fleet.fleet_position)
            game_pad.pad.title('Sea battle')
            gamer_choice = game_pad.create_pad()
            game_pad.pad.mainloop()
