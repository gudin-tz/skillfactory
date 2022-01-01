import random
from tkinter import *


class FleetCreating:
    """
    Класс создания флота
    """

    def __init__(self, pad_side):
        """
        Основная функция класса
        :param pad_side: размер игрового поля, указанный игроком
        """

        # Размер квадрата минимального игрового поля
        self.basic = 6
        # Список видов кораблей на игровом поле: x - (одноклеточные), y - (двуклеточные), z - (трехклеточные)
        self.fleet = [4, 2, 1]
        # Координаты каждой клетки игрового поля
        self.pad = []
        # Координаты каждого корабля
        self.fleet_position = []
        # Создаём счётчик для полчения общего количества кораблей на игровом поле
        self.ships_in_fleet = 0

        """
        Цикл, записывающий координаты каждой клетки в список
        """
        for i in range(pad_side):
            for j in range(pad_side):
                self.pad.append([i, j])

        # Запускаем цикл создания кораблей на игровом поле и запись их координат в список
        for i in range(len(self.fleet)):
            # Высчитываем количество кораблей в зависимости от количества мачт и выставленного размера игрового поля
            ships_by_mast = self.fleet[i] + self.fleet[i] * (pad_side - self.basic)
            # Увеличиваем счётчик количества кораблей на игровом поле
            self.ships_in_fleet += ships_by_mast
            # Запускаем цикл, вычисляющий положение каждого корабля
            for ship in range(ships_by_mast):
                # Задаём считчик попыток цикла ниже
                attempt = 0
                # Запускаем цикл, проверяющий клетки поля на предмет занятости, предел попыток - 10000
                while not self.ship_placement(i + 1) and attempt < 10000:
                    # Увеличиваем счётчик попыток
                    attempt += 1

    def ship_placement(self, nom):
        """
        Функция
        :param nom: количество мачт у текущего корабля
        :return: True - корабль создать можно, False - корабль создать нельзя
        """

        def side_check():
            """
            Функция, проверяющая, что корбль при выбранном положении не выйдет за пределы игрового поля
            :return: True - корабль помещается на игровом поле, False - корабль выходит за пределы игрового поля
            """

            if position[1] + nom > self.basic:
                return False
            return True

        def space_pad_check():
            """
            Функция проверки, что корабль не займет уже занятые клетки игрового поля
            :return: True - создать корабль можно, False - корабль создать нельзя
            """

            # Результат проверки координаты игрового поля на занятость
            result = True
            # Временный список для записи вычисляемых координат создаваемого корабля
            delta = []

            # Выполняем, если количество мачт больше 1
            if nom > 0:
                # Выполняем, если корабль требуется создать вертикально
                if direction == 0:
                    # Запускаем цикл по количеству мачт
                    for i in range(nom):
                        # Вычисляем текущую координату клетки, в которой предполается создать корабль
                        position_check = [position[0], position[1] + i]
                        # Проверяем, что текущая координата не занята
                        result = result * (position_check in self.pad)
                        # Записываем координаты текущей клетки в список
                        delta.append(position_check)
                        # Чтобы корабли не липли друг к другу, пишем координаты клеток справа и слева от корабля
                        delta.append([position[0] + 1, position[1]])
                        delta.append([position[0] - 1, position[1]])
                        # Чтобы корабли не липли друг к другу пишем координаты клеток снизу и сверху от корабля
                        # Выполняем, если клетка первая из проверяемых
                        if i == 0:
                            delta.append([position[0], position[1] - 1])
                        # Выполняем, если клетка последняя из проверяемых
                        elif i == nom:
                            delta.append([position[0], position[1] + 1])
                    # Выполняем, если результат от проверки незанятости клетки положительный
                    if result:
                        # Добавляем проверенный корабль в список флота: направление, количество мачт, координаты
                        self.fleet_position.append([direction, nom, position])
                        # Запускаем цикл по временному списку координат
                        for el in delta:
                            # Выполняем, если клетка не выходит за пределы игрового поля
                            if el in self.pad:
                                # Удаляем координату из списка игрового поля, помечая её как занятую
                                self.pad.remove(el)
                        # Возвращаем, что создать корабль можно
                        return True
                # Выполняем, если корабль требуется создать горизонтально
                if direction == 1:
                    # Запускаем цикл по количеству мачт
                    for i in range(nom):
                        # Вычисляем текущую координату клетки, в которой предполается создать корабль
                        position_check = [position[0] + i, position[1]]
                        # Проверяем, что текущая координата не занята
                        result = result * (position_check in self.pad)
                        # Записываем координаты текущей клетки в список
                        delta.append(position_check)
                        # Чтобы корабли не липли друг к другу, пишем координаты клеток справа и слева от корабля
                        delta.append([position[0], position[1] + 1])
                        delta.append([position[0], position[1] - 1])
                        # Чтобы корабли не липли друг к другу пишем координаты клеток снизу и сверху от корабля
                        # Выполняем, если клетка первая из проверяемых
                        if i == 0:
                            delta.append([position[0] - 1, position[1]])
                        # Выполняем, если клетка последняя из проверяемых
                        elif i == nom:
                            delta.append([position[0] + 1, position[1]])
                    # Выполняем, если результат от проверки незанятости клетки положительный
                    if result:
                        # Добавляем проверенный корабль в список флота: направление, количество мачт, координаты
                        self.fleet_position.append([direction, nom, position])
                        # Запускаем цикл по временному списку координат
                        for el in delta:
                            # Выполняем, если клетка не выходит за пределы игрового поля
                            if el in self.pad:
                                # Удаляем координату из списка игрового поля, помечая её как занятую
                                self.pad.remove(el)
                        # Возвращаем, что создать корабль можно
                        return True
            # Выполняем, если у корабля всего одна мачта
            else:
                # Добавляем проверенный корабль в список флота: направление, количество мачт, координаты
                self.fleet_position.append([direction, nom, position])
                # Удаляем координату из списка игрового поля, помечая её как занятую
                self.pad.remove(position)
                # Возвращаем, что создать корабль можно
                return True

            # Возвращаем, что создать корабль нельзя
            return False

        # Рандомный выбор положения корабля на игровом поле: 0 - вертикально, 1 - горизонтально
        direction = random.randint(0, 1)
        # Рандомный выбор координаты на игровом поле
        position = random.choice(self.pad)

        # Выполняем, если корабль помещается на игровом поле
        if side_check():
            # Выполняем, если при создании корабля в используемом месте игрового поля нет занятых клеток
            if space_pad_check():
                # Возвращаем список из корабля и его координат
                return [self.ships_in_fleet, self.fleet_position]

        # Возвращаем, что корабль не помещается на игровом поле
        return False


class GamePad:
    """
    Класс создания графического игрового поля
    """

    def __init__(self, gamer, pad_side, fleet_position):
        """
        Основная функция класса
        :param gamer: игрок или ИИ
        :param pad_side: размер игрового поля, указанный игроком
        :param fleet_position: координаты флота
        """

        # Инициируем Tkinter в переменную
        self.pad = Tk()
        # Инициируем игрока в переменную
        self.gamer = gamer
        # Инициируем указанный игроком размер игрового поля в переменную
        self.pad.side = pad_side
        # Создаём пустой список ячеек игрового поля
        self.pad.cells = []
        # Создаём пустой список кнопок игровокго поля
        self.buttons_ai = []
        #
        self.active = None
        # Инициируем координаты флота в переменную
        self.fleet_position = fleet_position

    def create_pad(self):
        """
        Функция создания игрового поля
        :return: ничего не возвращает
        """

        def set_ship():
            """
            Функция установки корабля на игровом поле
            :return: ничего не возвращает
            """

            # Запускаем цикл по каждому кораблю во флоте
            for ship in self.fleet_position:
                # Выполняем, если корабль размещается вертикально
                if ship[0] == 0:
                    # Запускаем цикл по количеству мачт
                    for x in range(ship[1]):
                        # Создаём Label для части корпуса корабля
                        lbl = Label(text=ship[1], bg='red', relief="groove")
                        # Прописываем Label на игровом поле
                        lbl.grid(row=ship[2][0], column=ship[2][1] + x, sticky='nwse')
                # Выполняем, если корабль размещается горизонтально
                else:
                    # Запускаем цикл по количеству мачт
                    for x in range(ship[1]):
                        # Создаём Label для части корпуса корабля
                        lbl = Label(text=ship[1], bg='red', relief="groove")
                        # Прописываем Label на игровом поле
                        lbl.grid(row=ship[2][0] + x, column=ship[2][1], sticky='nwse')

        def cell_press(a, b):
            """
            Функция реакции кнопки игрового поля на нажатие
            :param a: координата по горизонтали
            :param b: координата по вертикали
            :return: ничего не возвращает
            """

            # Разрушаем кнопку при нажатии
            self.buttons_ai[a * self.pad.side + b].destroy()

        # Запускаем цикл по размеру стороны игрового поля
        for i in range(self.pad.side):
            # Запускаем цикл по размеру стороны игрового поля
            for j in range(self.pad.side):
                # Устанавливаем высоту строки игрового поля
                self.pad.rowconfigure(i, minsize=30)
                # Устанавливаем ширину столбца игрового поля
                self.pad.columnconfigure(j, minsize=30)
                # Вписываем Label в ячейку
                Label(borderwidth="1", relief="sunken", width="4", height="2", bg="blue").grid(row=i, column=j)

        # Прописываем корабль на игровом поле
        set_ship()

        # Запускаем цикл по размеру стороны игрового поля
        for i in range(self.pad.side):
            # Запускаем цикл по размеру стороны игрового поля
            for j in range(self.pad.side*2 + 1):
                # Выполняем, если игровое поле строится для человека
                if self.gamer == 'human':
                    if j == self.pad.side:
                        _relief = "flat"
                    else:
                        _relief = "groove"
                    # Создаём Button для части корпуса корабля
                    button = Button(borderwidth="1", relief=_relief, command=lambda a=i, b=j: cell_press(a, b))
                    # Прописываем Button на игровом поле и добавляеи оазделитель между игровыми полями
                    if j != self.pad.side:
                        button.grid(row=i, column=j, sticky='nwse')
                    else:
                        Label(relief="groove", width="2", height="2", bg="yellow").grid(row=i, column=j, sticky='nwse')

                    # Добавляем Button в список кнопок игрового поля
                    if j < self.pad.side:
                        self.buttons_ai.append(button)
                # Добавляем координату клетки игрового поля в список
                if j < self.pad.side:
                    self.pad.cells.append((str(i) + ',' + str(j)))
