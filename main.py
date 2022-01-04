#!/usr/bin/python3
import sys

from library import classes

if __name__ == '__main__':

    # Задаём размер игрового поля
    side = 6
    # Создаём словарь флотов игроков
    fleets = {}

    # Запускаем цикл по игрокам
    for gamer in ['human', 'ai']:
        # Создаём флот игрока и пишем результат в переменную
        value = classes.FleetCreating(side)

        # Выполняем, если количество кораблей во флоте совпадает с аналогичным счётчиком
        if len(value.fleet_position) == value.ships_in_fleet:
            # Задаём игровое поле с флотом игрока
            game_pad = classes.GamePad(gamer, side, value.fleet_position)
            # Задаём имя игрового поля
            game_pad.pad.title('Sea battle')
            # Создаём игровое поле с флотом игрока
            gamer_choice = game_pad.create_pad()
            # Инициируем сделанные настройки для Tkinter
            game_pad.pad.mainloop()
        else:
            print(gamer + ': Корабли не помещаются на игровом поле. Перезапустите игру.')
            sys.exit()
